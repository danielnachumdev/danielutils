from ..conditional_variable import ConditionalVariable
from .....classes import frange
from ...supp import DiscreteRangeSupp
from ...operators import Operators


class Geometric(ConditionalVariable):

    def __hash__(self):
        return hash((self.__class__.__qualname__, self.p))

    def _supp(self):
        return DiscreteRangeSupp(frange(1, float("inf"), 1))

    def _evaluate(self, op, n) -> float:
        if op == Operators.EQ:
            return self.p * (1 - self.p) ** n
        elif op == Operators.NE:
            return 1 - self.evaluate(Operators.EQ, n)
        elif op == Operators.LT:
            return self.evaluate(Operators.GE, n)
        elif op == Operators.GT:
            return (1 - self.p) ** n
        elif op == Operators.GE:
            return (1 - self.p) ** (n - 1)
        elif op == Operators.LE:
            return 1 - self.evaluate(Operators.LT, n)
        else:
            raise RuntimeError("Unreachable Code")

    def __init__(self, p: float) -> None:
        self.p = p


Geo = Geometric

__all__ = [
    "Geometric",
    "Geo"
]
