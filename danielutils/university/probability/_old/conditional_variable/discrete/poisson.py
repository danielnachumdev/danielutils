from ..conditional_variable import ConditionalVariable
from university.probability._old.operators import Operators
from university.probability._old.supp import Supp


class Poisson(ConditionalVariable):
    @property
    def p(self):
        return self._p

    def __init__(self, p: float) -> None:
        self._p = p

    def _evaluate(self, op: Operators, val) -> float:
        pass

    def _supp(self) -> Supp:
        pass

    def __hash__(self):
        pass


Pois = Poisson
__all__ = [
    "Poisson",
    "Pois"
]
