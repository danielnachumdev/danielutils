from ..conditional_variable import ConditionalVariable
from ...supp import DiscreteRangeSupp
from .....classes import frange


class Uniform(ConditionalVariable):
    def _evaluate(self, op, val) -> float:
        return 1 / self._n

    def _supp(self) -> DiscreteRangeSupp:
        return DiscreteRangeSupp(frange(1, self._n + 1, 1))

    def __hash__(self):
        return hash((self.__class__.__qualname__, self._n))

    def __init__(self, n: int):
        self._n = n


Unif = Uniform

__all__ = [
    "Uniform",
    "Unif",
]
