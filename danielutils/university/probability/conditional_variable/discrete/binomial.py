from fractions import Fraction
from typing import Union
from math import factorial
from .discrete import DiscreteConditionalVariable
from ...supp import FrangeSupp
from ...operator import Operator
from .....better_builtins import frange
from ...protocols import ExpectedValueCalculable, VariableCalculable


def choose(n: int, k: int) -> Fraction:
    return Fraction(factorial(n), (factorial(k) * factorial(n - k)))


class Binomial(DiscreteConditionalVariable, ExpectedValueCalculable, VariableCalculable):
    def __init__(self, n: int, p: Union[float, Fraction]):
        super().__init__(p, FrangeSupp(frange(0, float("inf"))))
        self._n = n

    @property
    def n(self) -> int:
        return self._n

    def evaluate(self, k: int, op: Operator) -> Fraction:
        if not 0 <= k <= self.n:
            return Fraction(0, 1)

        if op == Operator.EQ:
            return choose(self.n, k) * ((1 - self.p) ** (self.n - k)) * (self.p ** k)
        assert False  # TODO
        return 1 - self.evaluate(k, op.inverse)

    def expected_value(self) -> Fraction:
        return self.n * self.p

    def variance(self) -> Fraction:
        return self.n * self.p * (1 - self.p)


__all__ = ['Binomial']
