from ..conditional_variable import ConditionalVariable
from ...operators import Operators
from ...supp import Supp, DiscreteRangeSupp


class Binomial(ConditionalVariable):
    @property
    def n(self) -> int:
        return self._n

    @property
    def p(self) -> float:
        return self._p

    def __init__(self, n: int, p: float) -> None:
        self._n = n
        self._p = p

    def _evaluate(self, op: Operators, val) -> float:
        pass

    def _supp(self) -> Supp:
        return DiscreteRangeSupp.from_explicit(1, float("inf"), 1)

    def __hash__(self):
        return hash((self.__class__, self.n, self.p))


Bin = Binomial
__all__ = [
    "Binomial",
    "Bin"
]
