from typing import Any

from ..conditional_variable import ConditionalVariable
from ...operator import Operator


class Bernoulli(ConditionalVariable):
    def evaluate(self, op: Operator, n: float) -> float:
        if op == Operator.EQ:
            if n == 1.0:
                return self.p
            if n == 0.0:
                return 1.0 - self.p
            return 0.0

        if op == Operator.NE:
            return 1.0 - self.evaluate(Operator.EQ, n)

        if op == Operator.GT:
            if n >= 1:
                return 0
            if n < 0:
                return 1
            return self.p

        if op == Operator.LE:
            return 1.0 - self.evaluate(Operator.GT, n)

        if op == Operator.LT:
            if n <= 0:
                return 0.0
            if n > 1:
                return 1.0
            return 1.0 - self.p

        if op == Operator.GE:
            return 1.0 - self.evaluate(Operator.LT, n)

        raise RuntimeError("Illegal State")

    @property
    def p(self) -> float:
        return self._p

    def __init__(self, p: float) -> None:
        self._p = p


__all__ = [
    "Bernoulli"
]
