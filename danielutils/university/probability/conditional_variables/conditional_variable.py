from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Callable, Any
from ..expressions import ProbabilityExpression, AccumulationExpression
from ..operator import Operator
from ..supp import Supp


class ConditionalVariable(ABC):
    OPERATOR_TYPE = Callable[['ConditionalVariable', Any], ProbabilityExpression]

    @staticmethod
    def _create_operator(op, reverse: bool = False) -> Callable[['ConditionalVariable', Any], ProbabilityExpression]:
        cls = AccumulationExpression
        # if op in {Operator.AND, Operator.GIVEN}:
        #     cls = AccumulationExpression

        def operator(self, other: Any) -> ProbabilityExpression:
            return cls(self, op, other)

        return operator

    __eq__: OPERATOR_TYPE = _create_operator(Operator.EQ)
    __ne__: OPERATOR_TYPE = _create_operator(Operator.NE)
    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)

    __mul__: OPERATOR_TYPE = _create_operator(Operator.MUL)
    __truediv__: OPERATOR_TYPE = _create_operator(Operator.DIV)
    __and__: OPERATOR_TYPE = _create_operator(Operator.AND)
    __or__: OPERATOR_TYPE = _create_operator(Operator.GIVEN)
    __mod__: OPERATOR_TYPE = _create_operator(Operator.MODULUS)
    __pow__: OPERATOR_TYPE = _create_operator(Operator.POW)

    @abstractmethod
    def evaluate(self, other: Any, operator: Operator) -> Fraction:
        ...

    @property
    @abstractmethod
    def supp(self) -> Supp:
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


__all__ = [
    "ConditionalVariable"
]
