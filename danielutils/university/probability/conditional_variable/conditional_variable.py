from abc import ABC, abstractmethod,abstractproperty
from typing import Union, Any, Callable

from ..operators import Operators
from ....decorators import memo
from ....functions import isoftype
from ..supp import Supp
from ..accumulation_expression import AccumulationExpression

SelfT = Any


class ConditionalVariable(ABC):

    @property
    @memo
    def supp(self) -> Supp:
        return self._supp()

    def evaluate(self, op: Operators, n: int) -> float:
        return self._evaluate(op, n)

    @abstractmethod
    def _evaluate(self, op:Operators, val) -> float:
        pass

    @abstractmethod
    def _supp(self) -> Supp:
        pass

    @staticmethod
    def _create_operator(op: Operators) -> Callable[[SelfT, Any], Any]:
        def inner(self, other):
            if isinstance(other, AccumulationExpression):
                other.add_left(self, op)
                return other
            from ..conditional_expression import ConditionalWithValue, ConditionalWithConditional
            if isoftype(other, Union[int, float]):
                return ConditionalWithValue(self, op, other)
            elif isinstance(other, ConditionalVariable):
                return ConditionalWithConditional(self, op, other)
            raise NotImplementedError("Illegal state (?)")

        return inner

    __eq__ = _create_operator(Operators.EQ)
    __lt__ = _create_operator(Operators.LT)
    __le__ = _create_operator(Operators.LE)
    __ne__ = _create_operator(Operators.NE)
    __ge__ = _create_operator(Operators.GE)
    __gt__ = _create_operator(Operators.GT)

    @abstractmethod
    def __hash__(self):
        pass

    def __or__(self, other):
        return AccumulationExpression.from_raw(self, Operators.GIVEN, other)

    def __ror__(self, other):
        return AccumulationExpression.from_raw(other, Operators.GIVEN, self)

    def __and__(self, other):
        return AccumulationExpression.from_raw(self, Operators.AND, other)

    def __rand__(self, other):
        return AccumulationExpression.from_raw(other, Operators.AND, self)
