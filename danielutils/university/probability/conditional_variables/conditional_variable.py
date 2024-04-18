from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Callable, Any
from ..expressions import ProbabilityExpression, AccumulationExpression
from ..operator import Operator
from ..supp import Supp
from ..protocols import Evaluable


class ConditionalVariable(ABC):
    OPERATOR_TYPE = Callable[['ConditionalVariable', Any], Evaluable]

    @staticmethod
    def _create_operator(op: Operator, reverse: bool = False) -> Callable[['ConditionalVariable', Any], Evaluable]:
        def operator(self, other) -> Evaluable:
            lhs, rhs = self, other
            if reverse:
                lhs, rhs = rhs, lhs

            if isinstance(other, (int, float, Fraction)):
                return ProbabilityExpression(lhs, op, rhs)

            if isinstance(rhs, ProbabilityExpression):
                l = ProbabilityExpression(lhs, op, rhs.lhs)
                r = ProbabilityExpression(rhs.rhs, None, None)
                o = other.op
                return AccumulationExpression(l, o, r)

            raise NotImplementedError("Not Implemented")

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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def is_dependent(self, other) -> bool:
        if not isinstance(other, ConditionalVariable):
            return False
        return self is other

    def is_independent(self, other) -> bool:
        return not self.is_dependent(other)

    @abstractmethod
    def evaluate(self, other: Any, operator: Operator) -> Fraction:
        ...

    @abstractmethod
    def between(self, a, b, *args) -> Fraction:
        ...

    @property
    @abstractmethod
    def supp(self) -> Supp:
        ...

    @abstractmethod
    def is_equal(self, other) -> bool:
        ...


__all__ = [
    "ConditionalVariable"
]
