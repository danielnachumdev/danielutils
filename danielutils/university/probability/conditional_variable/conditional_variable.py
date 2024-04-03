from abc import ABC, abstractmethod
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

    def evaluate(self, op, n) -> float:
        if n not in self.supp:
            raise ValueError(f"{self.__class__.__qualname__} does not support {n}")
        return self._evaluate(op, n)

    @abstractmethod
    def _evaluate(self, op, val) -> float:
        pass

    @abstractmethod
    def _supp(self) -> Supp:
        pass

    @staticmethod
    def _create_operator(op: Operators) -> Callable[[SelfT, Any], Any]:
        def operator(self, other):
            if isinstance(other, AccumulationExpression):
                other.add_left(self, op)
                return other
            from ..conditional_expression import ConditionalWithValue, ConditionalWithConditional
            if isoftype(other, Union[int, float]):
                return ConditionalWithValue(self, op, other)
            elif isinstance(other, ConditionalVariable):
                return ConditionalWithConditional(self, op, other)

        return operator

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
        return AccumulationExpression(self, Operators.GIVEN, other)

    def __ror__(self, other):
        return AccumulationExpression(other, Operators.GIVEN, self)
