from fractions import Fraction

from .discrete import DiscreteConditionalVariable
from ...supp import DiscreteSupp
from ...operator import Operator
from ...protocols import ExpectedValueCalculable, VariableCalculable


class Bernoulli(DiscreteConditionalVariable, ExpectedValueCalculable, VariableCalculable):
    def evaluate(self, n: int, op: Operator) -> Fraction:
        if n not in self.supp:
            return 0

        if op == Operator.EQ:
            return self.p if n == 1 else 1 - self.p
        assert False  # TODO

        return 1 - self.evaluate(n, op.inverse)

    def __init__(self, p) -> None:
        super().__init__(p, DiscreteSupp(range(0, 2)))

    def expected_value(self) -> Fraction:
        return self.p

    def variance(self) -> Fraction:
        return self.p * (1 - self.p)


__all__ = ['Bernoulli']
