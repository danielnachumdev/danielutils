from fractions import Fraction

from .discrete import DiscreteConditionalVariable
from ...supp import FrangeSupp
from ...operator import Operator
from ...protocols import ExpectedValueCalculable, VariableCalculable


class Bernoulli(DiscreteConditionalVariable, ExpectedValueCalculable, VariableCalculable):
    def evaluate(self, n: int, op: Operator) -> Fraction:
        if op == Operator.EQ:
            return self.p if n == 1 else 1 - self.p
        if op == Operator.GE:
            if n <= 0:
                return Fraction(1, 1)
            if n == 1:
                return self.p
            return Fraction(0, 1)
        if op == Operator.LE:
            if n >= 1:
                return Fraction(1, 1)
            if n == 0:
                return 1 - self.p
            return Fraction(0, 1)

        return 1 - self.evaluate(n, op.inverse)

    def __init__(self, p) -> None:
        super().__init__(p, FrangeSupp(range(0, 2)))

    def expected_value(self) -> Fraction:
        return self.p

    def variance(self) -> Fraction:
        return self.p * (1 - self.p)


__all__ = ['Bernoulli']
