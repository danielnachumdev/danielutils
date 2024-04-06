from ..conditional_variable import ConditionalVariable
from .....classes import frange
from ...supp import DiscreteRangeSupp
from ...operators import Operators


class Geometric(ConditionalVariable):

    def __hash__(self):
        return hash((self.__class__.__qualname__, self.p))

    def _supp(self) -> DiscreteRangeSupp:
        return DiscreteRangeSupp(frange(1, float("inf"), 1))

    def _evaluate(self, op, n) -> float:
        if n > 0:
            if op == Operators.EQ:
                return self.p * (1 - self.p) ** n
            if op == Operators.GT:
                return (1 - self.p) ** n
            if op == Operators.GE:
                return self.evaluate(Operators.GT, n - 1)
            if op == Operators.NE:
                return 1 - self.evaluate(Operators.EQ, n)
            if op == Operators.LT:
                return 1 - self.evaluate(Operators.GE, n)
            if op == Operators.LE:
                return 1 - self.evaluate(Operators.GT, n)
            raise RuntimeError("Illegal State")
        else:
            if op in {Operators.EQ, Operators.LT, Operators.LE}:
                return 0
            if op in {Operators.GT, Operators.GE, Operators.NE}:
                return 1
            raise RuntimeError("Illegal State")

    def __init__(self, p: float) -> None:
        self.p = p


Geo = Geometric

__all__ = [
    "Geometric",
    "Geo"
]
