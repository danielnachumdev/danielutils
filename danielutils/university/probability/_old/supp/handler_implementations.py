def discrete_set_discrete_set(lhs, rhs):
    from .discrete_supp import DiscreteSetSupp
    return DiscreteSetSupp(lhs._obj.intersection(rhs._obj))


def discrete_set_discrete_range(lhs, rhs):
    from .discrete_supp import DiscreteSetSupp
    res: set = set()
    for o in lhs:
        if o in rhs:
            res.add(o)
    return DiscreteSetSupp(res)


def discrete_range_discrete_range(lhs, rhs):
    from .discrete_supp import DiscreteRangeSupp
    return DiscreteRangeSupp(lhs.inner.intersect(rhs.inner))


__all__ = [
    "discrete_set_discrete_range",
    "discrete_set_discrete_set",
    "discrete_range_discrete_range"
]
