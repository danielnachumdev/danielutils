from fractions import Fraction
from typing import Union

from .discrete import DiscreteConditionalVariable
from .binomial import Binomial
from ...operator import Operator
from ...supp import FrangeSupp
from .....better_builtins import frange


class BernoulliSum(DiscreteConditionalVariable):
    """Sum of iid Bernoulli variables; evaluates via Binomial."""

    def __init__(self, p: Union[float, Fraction], n: int) -> None:
        super().__init__(p, FrangeSupp(frange(0, n + 1)))
        self._n = n

    @property
    def n(self) -> int:
        return self._n

    def evaluate(self, k: int, op: Operator) -> Fraction:
        return Binomial(self._n, self.p).evaluate(k, op)

    def is_equal(self, other) -> bool:
        if not isinstance(other, BernoulliSum):
            return False
        return self.p == other.p and self._n == other._n


__all__ = ["BernoulliSum"]
