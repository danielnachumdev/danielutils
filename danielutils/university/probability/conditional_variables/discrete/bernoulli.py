from fractions import Fraction

from .discrete import DiscreteConditionalVariable
from ...supp import DiscreteSupp
from ...operator import Operator


class Bernoulli(DiscreteConditionalVariable):
    def evaluate(self, n: int, op: Operator) -> Fraction:
        if n not in self.supp:
            return 0

        if op == Operator.EQ:
            return self.p if n == 1 else 1 - self.p
        assert False  # TODO

        return 1 - self.evaluate(n, op.inverse)

    def __init__(self, p) -> None:
        super().__init__(p, DiscreteSupp(range(0, 2)))


__all__ = ['Bernoulli']
