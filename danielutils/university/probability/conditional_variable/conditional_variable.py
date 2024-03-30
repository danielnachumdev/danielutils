from abc import ABC, abstractmethod
from typing import Union

from ....decorators import memo
from ....functions import isoftype
from ..supp import Supp
from ..accumulation_expression import AccumulationExpression


class ConditionalVariable(ABC):

    @property
    @memo
    def supp(self) -> Supp:
        return self._supp()

    def evaluate(self, n) -> float:
        if n not in self.supp:
            raise ValueError(f"{self.__class__.__qualname__} does not support {n}")
        return self._evaluate(n)

    @abstractmethod
    def _evaluate(self, val) -> float:
        pass

    @abstractmethod
    def _supp(self) -> Supp:
        pass

    def __eq__(self, other):
        if isinstance(other, AccumulationExpression):
            other.add_left(self, AccumulationExpression.Operators.EQUALS)
            return other
        from ..conditional_expression import ConditionalWithValue, ConditionalWithConditional
        if isoftype(other, Union[int, float]):
            return ConditionalWithValue(self, other)
        elif isinstance(other, ConditionalVariable):
            return ConditionalWithConditional(self, other)

    @abstractmethod
    def __hash__(self):
        pass

    def __or__(self, other):
        return AccumulationExpression(self, AccumulationExpression.Operators.GIVEN, other)

    def __ror__(self, other):
        return AccumulationExpression(other, AccumulationExpression.Operators.GIVEN, self)
