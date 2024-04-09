from typing import Any

from .evaluable import Evaluable
from .operator import Operator


class ComplexExpression(Evaluable):
    @property
    def lhs(self) -> Evaluable:
        return self._lhs

    @property
    def op(self) -> Operator:
        return self._op

    @property
    def rhs(self) -> Evaluable:
        return self._rhs

    def __init__(self, lhs: Evaluable, op: Operator, rhs: Evaluable):
        self._lhs = lhs
        self._op = op
        self._rhs = rhs

    def evaluate(self) -> Any:
        pass


__all__ = [
    "ComplexExpression"
]
