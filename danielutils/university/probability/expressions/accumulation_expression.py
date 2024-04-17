from fractions import Fraction
from typing import Callable, Any

from .probability_expression import ProbabilityExpression
from ..operator import Operator


class AccumulationExpression(ProbabilityExpression):
    OPERATOR_TYPE = Callable[['AccumulationExpression', Any], ProbabilityExpression]

    @staticmethod
    def _create_operator(op, reverse: bool = False) -> Callable[['ConditionalVariable', Any], ProbabilityExpression]:
        def operator(self, other: Any) -> ProbabilityExpression:
            op
            assert False
            return self

        return operator

    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)
    __and__: OPERATOR_TYPE = _create_operator(Operator.AND)
    __or__: OPERATOR_TYPE = _create_operator(Operator.GIVEN)

    def evaluate(self) -> Fraction:
        pass

    def _insert_right(self,obj)->None:
        pass

    def _insert_left(self,obj)->None:
        pass

__all__ = [
    'AccumulationExpression'
]
