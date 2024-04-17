from fractions import Fraction
from typing import Union

from .discrete import DiscreteConditionalVariable
from ...operator import Operator
from .....classes import frange
from ...supp import DiscreteSupp
from ...protocols import ExpectedValueCalculable, VariableCalculable


class Geometric(DiscreteConditionalVariable, ExpectedValueCalculable, VariableCalculable):
    def __init__(self, p: Union[float, Fraction]):
        super().__init__(Fraction(p), DiscreteSupp(frange(1, float("inf"), 1)))

    def _is_edge_case(self, n: int, op: Operator) -> tuple[bool, Fraction]:
        if n <= 0 and op in Operator.greater_than_inequalities():
            return True, Fraction(1, 1)
        if n <= 0 and op in Operator.less_than_inequalities():
            return True, Fraction(0, 1)
        return False, Fraction(0, 1)

    def evaluate(self, n: int, op: Operator) -> Fraction:
        if (tup := self._is_edge_case(n, op))[0]:
            return tup[1]
        del tup

        if op == Operator.EQ:
            return (Fraction(1 - self.p) ** (n - 1)) * self.p
        if op == Operator.GT:
            return Fraction(1 - self.p) ** n
        if op == Operator.GE:
            return self.evaluate(n - 1, Operator.GT)
        return 1 - self.evaluate(n, op.inverse)

    def expected_value(self) -> Fraction:
        return Fraction(1, self.p)

    def variance(self) -> Fraction:
        return Fraction(1 - self.p, self.p ** 2)


__all__ = ['Geometric']
