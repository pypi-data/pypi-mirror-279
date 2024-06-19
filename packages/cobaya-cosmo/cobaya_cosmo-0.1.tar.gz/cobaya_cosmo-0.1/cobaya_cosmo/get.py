"""
Module to fetch internal and external packages.

Internal names are preferred.
"""

# TODO: use github_raw for latest updates if internet available. print warning: unstable

from cobaya_cosmo.external import external_list


def get_info_dict(name):
    err_msg_header = f"Could not get {name}: "
    # 1: check internal
    # ...
    # 2: check external
    observable = name.split(".")[0]
    full_name = name[len(observable) + 1:]
    try:
        obs_list = getattr(external_list, observable.lower())
    except AttributeError as excpt:
        raise ValueError(
            err_msg_header + f"Observable {observable} not recognized."
        ) from excpt
    try:
        # TODO: should it be case sensitive?
        info = obs_list[full_name]
    except KeyError as excpt:
        # TODO: did you mean...?
        raise ValueError(
            err_msg_header +
            f"Could not find likelihood {full_name} for observable {observable}."
        ) from excpt
    return info
