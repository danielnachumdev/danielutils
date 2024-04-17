from abc import ABC, abstractmethod
from typing import Callable, Any
from ..probability_expression import ProbabilityExpression
from ..operator import Operator
from ..supp import Supp


class ConditionalVariable(ABC):
    OPERATOR_TYPE = Callable[['ConditionalVariable', Any], ProbabilityExpression]

    @staticmethod
    def _create_operator(op) -> Callable[['ConditionalVariable', Any], ProbabilityExpression]:
        def operator(self, other: Any) -> ProbabilityExpression:
            return ProbabilityExpression(self, op, other)

        return operator

    __eq__: OPERATOR_TYPE = _create_operator(Operator.EQ)
    __ne__: OPERATOR_TYPE = _create_operator(Operator.NE)
    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)

    @abstractmethod
    def evaluate(self, other: Any, operator: Operator) -> float: ...

    @property
    @abstractmethod
    def supp(self) -> Supp: ...


__all__ = [
    "ConditionalVariable"
]
