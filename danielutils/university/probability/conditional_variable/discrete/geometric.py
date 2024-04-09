from ..conditional_variable import ConditionalVariable
from ...operator import Operator


class Geometric(ConditionalVariable):
    @property
    def p(self) -> float:
        return self.p

    def __init__(self, p: float):
        self._p = p

    def evaluate(self, op: Operator, n: float) -> float:
        if n > 0:
            if op == Operator.EQ:
                return self.p * (1 - self.p) ** n
            if op == Operator.GT:
                return (1 - self.p) ** n
            if op == Operator.GE:
                return self.evaluate(Operator.GT, n - 1)
            if op == Operator.NE:
                return 1 - self.evaluate(Operator.EQ, n)
            if op == Operator.LT:
                return 1 - self.evaluate(Operator.GE, n)
            if op == Operator.LE:
                return 1 - self.evaluate(Operator.GT, n)
        else:
            if op in {Operator.EQ, Operator.LT, Operator.LE}:
                return 0
            if op in {Operator.GT, Operator.GE, Operator.NE}:
                return 1
        raise RuntimeError("Illegal State")

__all__=[
    "Geometric"
]