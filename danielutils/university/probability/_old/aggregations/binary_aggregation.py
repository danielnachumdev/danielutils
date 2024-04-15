from ..operators import Operators


class BinaryAggregation:
    def __init__(self, lhs, op: Operators, rhs):
        self._lhs = lhs
        self._op = op
        self._rhs = rhs


__all__ = [
    "BinaryAggregation"
]
