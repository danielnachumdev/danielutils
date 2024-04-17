from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Callable, Any
from ..expressions import ProbabilityExpression, AccumulationExpression
from ..operator import Operator
from ..supp import Supp
from ..protocols import Evaluable


class ConditionalVariable(ABC):
    OPERATOR_TYPE = Callable[['ConditionalVariable', Any], ProbabilityExpression]

    @staticmethod
    def _create_operator(op: Operator, reverse: bool = False) -> Callable[['ConditionalVariable', Any], Any]:
        def operator(self, other):
            if isinstance(other, AccumulationExpression):
                other.add_left(self, op)
                return other

            if op in {Operator.AND, Operator.GIVEN}:
                lhs, rhs = self, other
                return AccumulationExpression.from_raw(self, op, rhs)

            if op in Operator.order_operators():
                return ProbabilityExpression(self, op, other)

            # if isinstance(other, (int, float)):
            #     return ConditionalWithValue(self, op, other)
            # elif isinstance(other, ConditionalVariable):
            #     return ConditionalWithConditional(self, op, other)
            raise NotImplementedError("Illegal state (?)")

        return operator

    __eq__: OPERATOR_TYPE = _create_operator(Operator.EQ)
    __ne__: OPERATOR_TYPE = _create_operator(Operator.NE)
    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)

    __or__: OPERATOR_TYPE = _create_operator(Operator.GIVEN)
    __ror__: OPERATOR_TYPE = _create_operator(Operator.GIVEN, reverse=True)
    __and__: OPERATOR_TYPE = _create_operator(Operator.AND)
    __rand__: OPERATOR_TYPE = _create_operator(Operator.AND, reverse=True)

    __mul__: OPERATOR_TYPE = _create_operator(Operator.MUL)
    __truediv__: OPERATOR_TYPE = _create_operator(Operator.DIV)
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
