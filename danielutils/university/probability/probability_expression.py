from typing import Any
from .protocols import Evaluable
from .operator import Operator
from fractions import Fraction


class ProbabilityExpression(Evaluable):
    def __init__(self, lhs: Evaluable, op: Operator, rhs: Any):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self) -> Fraction:
        return self.lhs.evaluate(self.rhs, self.op)


__all__ = ['ProbabilityExpression']
