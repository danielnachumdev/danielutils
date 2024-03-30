from ..conditional_variable import ConditionalVariable
from .....classes import frange
from ...supp import DiscreteRangeSupp

class Geometric(ConditionalVariable):

    def __hash__(self):
        return hash((self.__class__.__qualname__, self.p))

    def _supp(self):
        return DiscreteRangeSupp(frange(1, float("inf"), 1))

    def _evaluate(self, n) -> float:
        return self.p * (1 - self.p) ** n

    def __init__(self, p: float) -> None:
        self.p = p


Geo = Geometric

__all__ = [
    "Geometric",
    "Geo"
]
