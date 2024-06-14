from typing import Type

from frozendict import frozendict

from hgraph import compute_node, add_, TS, KEYABLE_SCALAR, SCALAR, sub_, getitem_, min_, max_, sum_, str_, graph, zero, \
    AUTO_RESOLVE, TSL, SIZE, WiringError


@compute_node
def union_frozendicts(lhs: TS[frozendict[KEYABLE_SCALAR, SCALAR]],
                      rhs: TS[frozendict[KEYABLE_SCALAR, SCALAR]]) -> TS[frozendict[KEYABLE_SCALAR, SCALAR]]:
    """
    Combine two timeseries of frozendicts
    """
    return lhs.value | rhs.value


@compute_node(overloads=sub_)
def sub_frozendicts(lhs: TS[frozendict[KEYABLE_SCALAR, SCALAR]],
                    rhs: TS[frozendict[KEYABLE_SCALAR, SCALAR]]) -> TS[frozendict[KEYABLE_SCALAR, SCALAR]]:
    """
    Return the difference of the two frozendicts (by key)
    """
    return frozendict({k: v for k, v in lhs.value.items() if k not in rhs.value})


@compute_node(overloads=getitem_)
def getitem_frozendict(ts: TS[frozendict[KEYABLE_SCALAR, SCALAR]],
                       key: TS[KEYABLE_SCALAR],
                       default_value: TS[SCALAR] = None) -> TS[SCALAR]:
    """
    Retrieve the dict item by key from the timeseries of scalar frozen dicts
    """
    default = default_value.value if default_value.valid else None
    return ts.value.get(key.value, default)


@graph(overloads=min_)
def min_frozendict(*ts: TSL[TS[frozendict[KEYABLE_SCALAR, SCALAR]], SIZE],
                   default_value: TS[SCALAR] = None) -> TS[SCALAR]:
    if len(ts) == 1:
        return min_frozendict_unary(ts[0], default_value)
    else:
        raise WiringError(f"Cannot compute min of {len(ts)} frozendicts")


@compute_node
def min_frozendict_unary(ts: TS[frozendict[KEYABLE_SCALAR, SCALAR]], default_value: TS[SCALAR] = None) -> TS[SCALAR]:
    """
    Return the minimum value in the frozendict
    If the frozendict is empty, the default value is returned
    """
    return min(ts.value.values(), default=default_value.value)


@graph(overloads=max_)
def max_frozendict(*ts: TSL[TS[frozendict[KEYABLE_SCALAR, SCALAR]], SIZE],
                   default_value: TS[SCALAR] = None) -> TS[SCALAR]:
    if len(ts) == 1:
        return max_frozendict_unary(ts[0], default_value)
    else:
        raise WiringError(f"Cannot compute max of {len(ts)} frozen dicts")


@compute_node
def max_frozendict_unary(ts: TS[frozendict[KEYABLE_SCALAR, SCALAR]], default_value: TS[SCALAR] = None) -> TS[SCALAR]:
    """
    Return the maximum value in the frozendict
    If the frozendict is empty, the default value is returned
    """
    return max(ts.value.values(), default=default_value.value)


@graph(overloads=sum_)
def sum_frozendict(*ts: TSL[TS[frozendict[KEYABLE_SCALAR, SCALAR]], SIZE],
                   tp: Type[TS[SCALAR]] = AUTO_RESOLVE) -> TS[SCALAR]:
    if len(ts) == 1:
        return _sum_frozendict_unary(ts[0], zero(tp, sum_))
    else:
        raise WiringError(f"Cannot compute sum of {len(ts)} frozen dicts")


@compute_node
def _sum_frozendict_unary(ts: TS[frozendict[KEYABLE_SCALAR, SCALAR]], zero_ts: TS[SCALAR]) -> TS[SCALAR]:
    """
    Return the sum of values in the frozendict value of the timeseries
    If the frozendict is empty, the default value is returned
    """
    return sum(ts.value.values(), start=zero_ts.value)


@compute_node(overloads=str_)
def str_frozendict(ts: TS[frozendict[KEYABLE_SCALAR, SCALAR]]) -> TS[str]:
    return str(dict(ts.value))
