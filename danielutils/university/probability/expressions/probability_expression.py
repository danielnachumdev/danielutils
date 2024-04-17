from typing import Any, Callable
from ..protocols import Evaluable
from ..operator import Operator
from fractions import Fraction
from .accumulation_expression import AccumulationExpression


class ProbabilityExpression(Evaluable):
    OPERATOR_TYPE = Callable[['ProbabilityExpression', Any], 'AccumulationExpression']

    def __init__(self, lhs: Evaluable, op: Operator, rhs: Any):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    @staticmethod
    def _create_operator(op, reverse: bool = False) -> Callable[['AccumulationExpression', Any], 'Evaluable']:
        def operator(self, other: Any) -> 'Evaluable':
            if op in {Operator.GIVEN, Operator.AND}:
                assert False
            else:
                lhs = self
                rhs = ProbabilityExpression(self.lhs, op, other)
                return AccumulationExpression(lhs, Operator.AND, rhs)

        return operator

    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)
    __and__: OPERATOR_TYPE = _create_operator(Operator.AND)
    __or__: OPERATOR_TYPE = _create_operator(Operator.GIVEN)

    def evaluate(self) -> Fraction:
        return self.lhs.evaluate(self.rhs, self.op)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.lhs} {self.op.value} {self.rhs})"

    @property
    def inverse(self) -> 'ProbabilityExpression':
        return ProbabilityExpression(self.lhs, self.op.inverse, self.rhs)


__all__ = [
    'ProbabilityExpression',
]
