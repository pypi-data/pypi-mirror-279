import os
from multiprocessing.pool import ThreadPool

import numpy as np

from bdpn import bd_model
from bdpn.formulas import get_log_p, get_c1, get_c2, get_E, get_log_ppb, get_log_pn, get_log_ppb_from_p_pn, \
    get_u, get_log_no_event, get_log_ppa, get_log_ppa_from_ppb, get_log_pb
from bdpn.parameter_estimator import optimize_likelihood_params, rescale_log
from bdpn.tree_manager import TIME, read_forest, annotate_forest_with_time

PARAMETER_NAMES = np.array(['la', 'psi', 'partner_psi', 'p', 'pn'])

DEFAULT_LOWER_BOUNDS = [bd_model.DEFAULT_MIN_RATE, bd_model.DEFAULT_MIN_RATE, bd_model.DEFAULT_MIN_RATE,
                        bd_model.DEFAULT_MIN_PROB, bd_model.DEFAULT_MIN_PROB]
DEFAULT_UPPER_BOUNDS = [bd_model.DEFAULT_MAX_RATE, bd_model.DEFAULT_MAX_RATE, bd_model.DEFAULT_MAX_RATE * 1e3,
                        bd_model.DEFAULT_MAX_PROB, bd_model.DEFAULT_MAX_PROB]


def log_sum(log_summands):
    """
    Takes [logX1, ..., logXk] as input and returns log(X1 + ... + Xk) as output, 
    while taking care of potential under/overflow.
    
    :param log_summands: an array of summands in log form
    :return: log of the sum
    """
    result = np.array(log_summands, dtype=np.float64)
    factors = rescale_log(result)
    return np.log(np.sum(np.exp(result))) - factors


def log_subtraction(log_minuend, log_subtrahend):
    """
    Takes logX1 and logX2 as input and returns log(X1 - X2) as output,
    while taking care of potential under/overflow.

    :param log_minuend: logX1 in the formula above
    :param log_subtrahend: logX2 in the formula above
    :return: log of the difference
    """
    # print(log_subtrahend, log_minuend)
    # assert (log_subtrahend < log_minuend)
    result = np.array([log_minuend, log_subtrahend], dtype=np.float64)
    factors = rescale_log(result)
    return np.log(np.sum(np.exp(result) * [1, -1])) - factors


def loglikelihood(forest, la, psi, phi, rho, upsilon, T=None, threads=1):
    annotate_forest_with_time(forest)
    T = get_T(T, forest)

    c1 = get_c1(la=la, psi=psi, rho=rho)
    c2 = get_c2(la=la, psi=psi, c1=c1)

    log_la, log_psi, log_phi, log_rho, log_not_rho, log_ups, log_not_ups, log_2 = \
        np.log(la), np.log(psi), np.log(phi), np.log(rho), np.log(1 - rho), np.log(upsilon), \
            np.log(1 - upsilon), np.log(2)
    log_2_la = log_2 + log_la
    log_psi_rho_ups = log_psi + log_rho + log_ups
    log_psi_rho_not_ups = log_psi + log_rho + log_not_ups
    log_phi_ups = log_phi + log_ups
    log_phi_not_ups = log_phi + log_not_ups

    def process_node(node):
        """
        Calculate the loglikelihood density of this branch being unnotified, including the subtree
        and put it into node's annotation: 'lx' for internal nodes,
        'lxx' and 'lxn' (depending on whether the node notified) for tips.

        :param node: tree node whose children (if any) are already processed
        :return: void, add a node annotation
        """
        ti = getattr(node, TIME)
        tj = ti - node.dist

        E_tj = get_E(c1=c1, c2=c2, t=tj, T=T)
        E_ti = get_E(c1, c2, ti, T)

        log_p = get_log_p(c1=c1, t=tj, ti=ti, E_t=E_tj, E_ti=E_ti)
        log_pn = get_log_pn(la=la, psi=psi, t=tj, ti=ti)
        log_ppb = get_log_ppb_from_p_pn(log_p=log_p, log_pn=log_pn)
        log_ppa = get_log_ppa_from_ppb(log_ppb=log_ppb, psi=psi, phi=phi, t=tj, ti=ti)

        node.add_feature('log_ppb', log_ppb)
        node.add_feature('log_ppa', log_ppa)

        th = tj + (ti - tj) / 2
        E_th = get_E(c1, c2, th, T)
        E_T = get_E(c1, c2, T, T)

        log_bottom_standard = get_log_p(c1, th, ti, E_th, E_ti)
        log_no_event_th = get_log_no_event(la + psi, tj, th)
        log_top_ppb = log_subtraction(get_log_ppb(la, psi, c1, tj, th, E_tj, E_th), log_no_event_th)
        log_top_ppa = log_subtraction(get_log_ppa(la, psi, phi, c1, tj, th, E_tj, E_th),
                                      get_log_no_event(la + phi, tj, th))

        def get_log_top_pp_U_p_th_tr(notifier):
            tr = getattr(notifier, TIME)
            E_tr = get_E(c1, c2, tr, T)
            if th <= tr:
                U_p_tr = get_log_ppb(la, psi, c1, th, tr, E_th, E_tr) \
                         + log_sum([np.log(1 - np.exp(-psi * (tr - th))) + psi * (tr - th) + log_not_rho,
                                    get_log_ppa(la, psi, phi, c1, tr, T, E_tr, E_T)])
                return log_top_ppb, U_p_tr
            U_p_tr = get_log_ppa(la, psi, phi, c1, th, T, E_th, E_T)
            if tj >= tr:
                return log_top_ppa, U_p_tr
            return get_log_ppb(la, psi, c1, tj, tr, E_tj, E_tr) + \
                   log_subtraction(get_log_ppa(la, psi, phi, c1, tr, th, E_tr, E_th),
                                   get_log_no_event(la + phi, tr, th)), U_p_tr

        notifiers = getattr(node, 'notifiers')
        notifier2log_top_pp_U_p = {notifier: get_log_top_pp_U_p_th_tr(notifier)
                                   for notifier in notifiers}
        log_u_th = np.log(get_u(la, psi, c1, E_th))

        node.add_feature('log_p_standard',
                         {notifier: log_top_pp + (log_u_p_th_tr - log_u_th) + log_bottom_standard
                          for (notifier, (log_top_pp, log_u_p_th_tr)) in notifier2log_top_pp_U_p.items()})

        if node.is_leaf():
            log_bottom_n = get_log_pn(la, psi, th, ti)
            log_u_p_th_ti = get_log_ppb(la, psi, c1, th, ti, E_th, E_ti) \
                            + log_sum([np.log(1 - np.exp(-psi * (ti - th))) + psi * (ti - th) + log_not_rho,
                                       get_log_ppa(la, psi, phi, c1, ti, T, E_ti, E_T)])
            node.add_feature('log_p_n',
                             {notifier: log_top_pp
                                        + ((log_u_p_th_tr if getattr(notifier, TIME) < ti else log_u_p_th_ti)
                                           - log_u_th)
                                        + log_bottom_n
                              for (notifier, (log_top_pp, log_u_p_th_tr)) in notifier2log_top_pp_U_p.items()})

            log_top_standard = log_subtraction(get_log_p(c1, tj, th, E_tj, E_th), log_no_event_th)
            node.add_feature('log_standard_n',
                             log_top_standard + (log_u_p_th_ti - log_u_th) + log_bottom_n)

            th1 = tj + (ti - tj) / 3
            th2 = tj + 2 * (ti - tj) / 3
            E_th1 = get_E(c1, c2, th1, T)
            E_th2 = get_E(c1, c2, th2, T)
            log_top1_ppb = log_subtraction(get_log_ppb(la, psi, c1, tj, th1, E_tj, E_th1),
                                           get_log_no_event(la + psi, tj, th1))
            log_top1_ppa = log_subtraction(get_log_ppa(la, psi, phi, c1, tj, th1, E_tj, E_th1),
                                           get_log_no_event(la + phi, tj, th1))

            def get_log_top1_pp_U_p_th1_tr(notifier):
                tr = getattr(notifier, TIME)
                E_tr = get_E(c1, c2, tr, T)
                if th1 <= tr:
                    U_p_th1_tr = get_log_ppb(la, psi, c1, th1, tr, E_th1, E_tr) \
                                 + log_sum([np.log(1 - np.exp(-psi * (tr - th1))) + psi * (tr - th1) + log_not_rho,
                                            get_log_ppa(la, psi, phi, c1, tr, T, E_tr, E_T)])
                    return log_top1_ppb, U_p_th1_tr
                U_p_th1_tr = get_log_ppa(la, psi, phi, c1, th1, T, E_th1, E_T)
                if tj >= tr:
                    return log_top1_ppa, U_p_th1_tr
                return get_log_ppb(la, psi, c1, tj, tr, E_tj, E_tr) + \
                       log_subtraction(get_log_ppa(la, psi, phi, c1, tr, th1, E_tr, E_th1),
                                       get_log_no_event(la + phi, tr, th1)), U_p_th1_tr

            notifier2log_top1_pp_U_p_th1_tr = {notifier: get_log_top1_pp_U_p_th1_tr(notifier)
                                               for notifier in notifiers}
            log_u_th1 = np.log(get_u(la, psi, c1, E_th1))
            log_u_th2 = np.log(get_u(la, psi, c1, E_th2))
            log_u_p_th2_ti = get_log_ppb(la, psi, c1, th2, ti, E_th2, E_ti) \
                             + log_sum([np.log(1 - np.exp(-psi * (ti - th2))) + psi * (ti - th2) + log_not_rho,
                                        get_log_ppa(la, psi, phi, c1, ti, T, E_ti, E_T)])

            log_top2_standard = log_subtraction(get_log_p(c1, th1, th2, E_th1, E_th2),
                                                get_log_no_event(la + psi, th1, th2))
            node.add_feature('log_p_standard_n',
                             {notifier: log_top1_pp + (log_u_p_th1_tr - log_u_th1)
                                        + log_top2_standard + (log_u_p_th2_ti - log_u_th2)
                                        + get_log_pn(la, psi, th2, ti)
                              for (notifier, (log_top1_pp, log_u_p_th1_tr)) in notifier2log_top1_pp_U_p_th1_tr.items()})

            node.add_feature('lxx', log_sum([log_p + log_psi_rho_not_ups,
                                             getattr(node, 'log_standard_n') + log_psi_rho_ups]))
            node.add_feature('lxn', log_pn + log_psi_rho_ups)

            def get_lnx(notifier):
                tr = getattr(notifier, TIME)
                E_tr = get_E(c1, c2, tr, T)
                log_non_hidden_partner = (log_ppa + log_phi_not_ups) if tr <= tj \
                    else ((log_ppb + log_psi_rho_not_ups) if tr >= ti else
                          (get_log_ppb(la, psi, c1, tj, tr, E_tj, E_tr)
                           + get_log_ppa(la, psi, phi, c1, tr, ti, E_tr, E_ti)
                           + log_phi_not_ups))
                return log_sum([log_non_hidden_partner,
                                getattr(node, 'log_p_standard')[notifier] + log_psi_rho_not_ups,
                                getattr(node, 'log_p_n')[notifier] + log_psi_rho_ups,
                                getattr(node, 'log_p_standard_n')[notifier] + log_psi_rho_ups])

            node.add_feature('lnx', {notifier: get_lnx(notifier) for notifier in notifiers})

            log_pb = get_log_pb(la, phi, tj, ti)

            def get_lnn(notifier):
                tr = getattr(notifier, TIME)
                if tr <= tj:
                    return log_pb + log_phi_ups
                if tr >= ti:
                    return log_pn + log_psi_rho_ups
                return get_log_pn(la, psi, tj, tr) + get_log_pb(la, phi, tr, ti) + log_phi_ups

            node.add_feature('lnn', {notifier: get_lnn(notifier) for notifier in notifiers})
            return

        i0, i1 = node.children
        is_tip0, is_tip1 = i0.is_leaf(), i1.is_leaf()

        branch = log_p + log_2_la

        def get_p_branches(notifier):
            tr = getattr(notifier, TIME)
            E_tr = get_E(c1, c2, tr, T)
            observed_branch = log_ppa if tr <= tj \
                else (log_ppb if tr >= ti else
                      (get_log_ppb(la, psi, c1, tj, tr, E_tj, E_tr)
                       + get_log_ppa(la, psi, phi, c1, tr, ti, E_tr, E_ti)))
            return observed_branch + log_la, getattr(node, 'log_p_standard')[notifier] + log_2_la

        notifier2branches = {notifier: get_p_branches(notifier) for notifier in notifiers}

        if not is_tip0 and not is_tip1:
            node.add_feature('lx', branch + getattr(i0, 'lx') + getattr(i1, 'lx'))

            def get_ln(notifier):
                observed_br, mixed_br = notifier2branches[notifier]
                return log_sum([observed_br + log_sum([getattr(i0, 'ln')[notifier] + getattr(i1, 'lx'),
                                                      getattr(i0, 'lx') + getattr(i1, 'ln')[notifier]]),
                                mixed_br + getattr(i0, 'lx') + getattr(i1, 'lx')])

            node.add_feature('ln', {notifier: get_ln(notifier) for notifier in notifiers})
            return


        ti0, ti1 = getattr(i0, TIME), getattr(i1, TIME)

        if is_tip0 and is_tip1:
            node.add_feature('lx', branch + log_sum([getattr(i0, 'lxx') + getattr(i1, 'lxx'),
                                                     getattr(i0, 'lxn') + getattr(i1, 'lnx')[i0],
                                                     getattr(i0, 'lnx')[i1] + getattr(i1, 'lxn'),
                                                     getattr(i0, 'lnn')[i1] + getattr(i1, 'lnn')[i0]]))

            def get_ln(notifier):
                tr = getattr(notifier, TIME)
                observed_br, mixed_br = notifier2branches[notifier]
                first_i0_r = i0 if ti0 < tr else notifier
                first_i1_r = i1 if ti1 < tr else notifier
                return log_sum([observed_br + log_sum([getattr(i0, 'lnx')[first_i1_r] + getattr(i1, 'lxn'),
                                                       getattr(i0, 'lnn')[first_i1_r] + getattr(i1, 'lnn')[i0],
                                                       getattr(i0, 'lxn') + getattr(i1, 'lnx')[first_i0_r],
                                                       getattr(i0, 'lnn')[i1] + getattr(i1, 'lnn')[first_i0_r],
                                                       getattr(i0, 'lnn')[notifier] + getattr(i1, 'lnx')[i0],
                                                       getattr(i0, 'lnx')[i1] + getattr(i1, 'lnn')[notifier],
                                                       getattr(i0, 'lnx')[notifier] + getattr(i1, 'lxx'),
                                                       getattr(i0, 'lxx') + getattr(i1, 'lnx')[notifier]]
                                                      ),
                                mixed_br + log_sum([getattr(i0, 'lnx')[i1] + getattr(i1, 'lxn'),
                                                    getattr(i0, 'lnn')[i1] + getattr(i1, 'lnn')[i0],
                                                    getattr(i0, 'lxn') + getattr(i1, 'lnx')[i0],
                                                    getattr(i0, 'lxx') + getattr(i1, 'lxx')])
                                ])

            node.add_feature('ln', {notifier: get_ln(notifier) for notifier in notifiers})

            return

        # i0 is a tip and i1 is internal
        if is_tip1:
            i0, i1 = i1, i0
            ti0, ti1 = ti1, ti0
        node.add_feature('lx', branch + log_sum([getattr(i0, 'lxx') + getattr(i1, 'lx'),
                                                 getattr(i0, 'lxn') + getattr(i1, 'ln')[i0]]))

        def get_ln(notifier):
            tr = getattr(notifier, TIME)
            observed_br, mixed_br = notifier2branches[notifier]
            first_i0_r = i0 if ti0 < tr else notifier
            return log_sum([observed_br + log_sum([getattr(i0, 'lnn')[notifier] + getattr(i1, 'ln')[i0],
                                                   getattr(i0, 'lnx')[notifier] + getattr(i1, 'lx'),
                                                   getattr(i0, 'lxn') + getattr(i1, 'ln')[first_i0_r],
                                                   getattr(i0, 'lxx') + getattr(i1, 'ln')[notifier]]
                                                  ),
                            mixed_br + log_sum([getattr(i0, 'lxn') + getattr(i1, 'ln')[i0],
                                                getattr(i0, 'lxx') + getattr(i1, 'lx')])
                            ])

        node.add_feature('ln', {notifier: get_ln(notifier) for notifier in notifiers})

    def process_tree(tree):
        all_tips = set(tree.iter_leaves())

        for node in tree.traverse('postorder'):
            ext_tips = (all_tips - {node}) if node.is_leaf() \
                else set.intersection(*(getattr(_, 'notifiers') for _ in node.children))
            node.add_feature('notifiers', ext_tips)
            process_node(node)
        return getattr(tree, 'lx' if not tree.is_leaf() else 'lxx')

    if threads > 1 and len(forest) > 1:
        with ThreadPool(processes=threads) as pool:
            result = sum(pool.map(func=process_tree, iterable=forest, chunksize=max(1, len(forest) // threads + 1)))
    else:
        result = sum(process_tree(tree) for tree in forest)

    u = get_u(la, psi, c1, E_t=get_E(c1=c1, c2=c2, t=0, T=T))
    result += len(forest) * u / (1 - u) * np.log(u)
    # print(la, psi, phi, rho, upsilon, '-->', result)
    return result


def get_T(T, forest):
    if T is None:
        T = 0
        for tree in forest:
            T = max(T, max(getattr(_, TIME) for _ in tree))
    return T


def save_results(vs, cis, log, ci=False):
    os.makedirs(os.path.dirname(os.path.abspath(log)), exist_ok=True)
    with open(log, 'w+') as f:
        f.write(',{}\n'.format(','.join(['R0', 'infectious time', 'sampling probability', 'notification probability',
                                         'removal time after notification',
                                         'transmission rate', 'removal rate', 'partner removal rate'])))
        la, psi, phi, rho, rho_p = vs
        R0 = la / psi
        rt = 1 / psi
        prt = 1 / phi
        (la_min, la_max), (psi_min, psi_max), (psi_p_min, psi_p_max), (rho_min, rho_max), (rho_p_min, rho_p_max) = cis
        R0_min, R0_max = la_min / psi, la_max / psi
        rt_min, rt_max = 1 / psi_max, 1 / psi_min
        prt_min, prt_max = 1 / psi_p_max, 1 / psi_p_min
        f.write('value,{}\n'.format(','.join(str(_) for _ in [R0, rt, rho, rho_p, prt, la, psi, phi])))
        if ci:
            f.write('CI_min,{}\n'.format(
                ','.join(str(_) for _ in [R0_min, rt_min, rho_min, rho_p_min, prt_min, la_min, psi_min, psi_p_min])))
            f.write('CI_max,{}\n'.format(
                ','.join(str(_) for _ in [R0_max, rt_max, rho_max, rho_p_max, prt_max, la_max, psi_max, psi_p_max])))


def main():
    """
    Entry point for tree parameter estimation with the BDPN model with command-line arguments.
    :return: void
    """
    import argparse

    parser = \
        argparse.ArgumentParser(description="Estimated BDPN parameters.")
    parser.add_argument('--la', required=False, default=None, type=float, help="transmission rate")
    parser.add_argument('--psi', required=False, default=None, type=float, help="removal rate")
    parser.add_argument('--p', required=False, default=None, type=float, help='sampling probability')
    parser.add_argument('--pn', required=False, default=None, type=float, help='notification probability')
    parser.add_argument('--phi', required=False, default=None, type=float, help='partner removal rate')
    parser.add_argument('--log', required=True, type=str, help="output log file")
    parser.add_argument('--nwk', required=True, type=str, help="input tree file")
    parser.add_argument('--upper_bounds', required=False, type=float, nargs=5,
                        help="upper bounds for parameters (la, psi, phi, p, pn)", default=DEFAULT_UPPER_BOUNDS)
    parser.add_argument('--lower_bounds', required=False, type=float, nargs=5,
                        help="lower bounds for parameters (la, psi, phi, p, pn)", default=DEFAULT_LOWER_BOUNDS)
    parser.add_argument('--ci', action="store_true", help="calculate the CIs")
    params = parser.parse_args()

    # if os.path.exists(params.nwk.replace('.nwk', '.log')):
    #     df = pd.read_csv(params.nwk.replace('.nwk', '.log'))
    #     R, it, p, pn, rt = df.iloc[0, :5]
    #     psi = 1 / it
    #     la = R * psi
    #     phi = 1 / rt
    #     print('Real parameters: ', np.array([la, psi, phi, p, pn]))
    #     params.psi = psi

    if params.la is None and params.psi is None and params.p is None:
        raise ValueError('At least one of the BD model parameters (la, psi, p) needs to be specified '
                         'for identifiability')

    forest = read_forest(params.nwk)
    print('Read a forest of {} trees with {} tips in total'.format(len(forest), sum(len(_) for _ in forest)))
    vs, cis = infer(forest, **vars(params))

    save_results(vs, cis, params.log, ci=params.ci)


def loglikelihood_main():
    """
    Entry point for tree likelihood estimation with the BDPN model with command-line arguments.
    :return: void
    """
    import argparse

    parser = \
        argparse.ArgumentParser(description="Calculate BDPN likelihood on a given forest for given parameter values.")
    parser.add_argument('--la', required=True, type=float, help="transmission rate")
    parser.add_argument('--psi', required=True, type=float, help="removal rate")
    parser.add_argument('--p', required=True, type=float, help='sampling probability')
    parser.add_argument('--upsilon', required=True, type=float, help='notification probability')
    parser.add_argument('--phi', required=True, type=float, help='partner removal rate')
    parser.add_argument('--nwk', required=True, type=str, help="input tree file")
    params = parser.parse_args()

    forest = read_forest(params.nwk)
    lk = loglikelihood(forest, la=params.la, psi=params.psi, rho=params.p, phi=params.phi, upsilon=params.upsilon)
    print(lk)


def infer(forest, la=None, psi=None, phi=None, p=None, pn=None,
          lower_bounds=DEFAULT_LOWER_BOUNDS, upper_bounds=DEFAULT_UPPER_BOUNDS, ci=False, **kwargs):
    """
    Infers BDPN model parameters from a given forest.

    :param forest: list of one or more trees
    :param la: transmission rate
    :param psi: removal rate
    :param phi: partner removal rate
    :param p: sampling probability
    :param pn: partner notification probability
    :param lower_bounds: array of lower bounds for parameter values (la, psi, partner_psi, p, pn)
    :param upper_bounds: array of upper bounds for parameter values (la, psi, partner_psi, p, pn)
    :param ci: whether to calculate the CIs or not
    :return: tuple(vs, cis) of estimated parameter values vs=[la, psi, partner_psi, p, pn]
        and CIs ci=[[la_min, la_max], ..., [pn_min, pn_max]]. In the case when CIs were not set to be calculated,
        their values would correspond exactly to the parameter values.
    """
    if la is None and psi is None and p is None:
        raise ValueError('At least one of the BD model parameters (la, psi, p) needs to be specified '
                         'for identifiability')
    bounds = np.zeros((5, 2), dtype=np.float64)
    bounds[:, 0] = lower_bounds
    bounds[:, 1] = upper_bounds
    vs, _ = bd_model.infer(forest, la=la, psi=psi, p=p,
                           lower_bounds=bounds[[0, 1, 3], 0], upper_bounds=bounds[[0, 1, 3], 1], ci=False)
    start_parameters = np.array([vs[0], vs[1], vs[1] * 10 if phi is None or phi < 0 else phi,
                                 vs[-1], 0.5 if pn is None or pn <= 0 or pn > 1 else pn])
    input_params = np.array([la, psi, phi, p, pn])
    print('Fixed input parameter(s): {}'
          .format(', '.join('{}={:g}'.format(*_)
                            for _ in zip(PARAMETER_NAMES[input_params != None], input_params[input_params != None]))))
    print('Starting BDPN parameters: {}'.format(start_parameters))
    vs, cis, lk = optimize_likelihood_params(forest, input_parameters=input_params,
                                             loglikelihood=loglikelihood, bounds=bounds[input_params == None],
                                             start_parameters=start_parameters, cis=ci)
    print('Estimated BDPN parameters: {}'.format(vs))
    if ci:
        print('Estimated CIs:\n{}'.format(cis))
    return vs, cis


if '__main__' == __name__:
    main()
