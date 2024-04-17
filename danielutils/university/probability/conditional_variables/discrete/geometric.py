from fractions import Fraction
from typing import Union

from .discrete import DiscreteConditionalVariable
from ...operator import Operator
from .....classes import frange
from ...supp import DiscreteSupp


class Geometric(DiscreteConditionalVariable):
    def __init__(self, p: Union[float, Fraction]):
        super().__init__(Fraction(p), DiscreteSupp(frange(1, float("inf"), 1)))

    def evaluate(self, n: int, op: Operator) -> Fraction:
        if n not in self.supp:
            return Fraction(0, 1)
        if op == Operator.EQ:
            return (Fraction(1 - self.p) ** n) * self.p
        if op == Operator.GT:
            return Fraction(1 - self.p) ** n
        if op == Operator.GE:
            return self.evaluate(n - 1, Operator.GT)
        return 1 - self.evaluate(n, op.inverse)


__all__ = ['Geometric']
