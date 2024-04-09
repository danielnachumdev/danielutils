from .binary_aggregation import BinaryAggregation
from university.probability._old.operators import Operators


class BinaryAdditionBinaryAggregation(BinaryAggregation):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, Operators.ADD, rhs)


__all__ = [
    "BinaryAdditionBinaryAggregation"
]
