from abc import ABC, abstractmethod
from typing import Any

from ..funcs import ProbabilityFunction as P
from ..conditional_variable import ConditionalVariable
from ..accumulation_expression import AccumulationExpression
from ..operators import Operators
from ....data_structures import BinaryNode


class ConditionalExpression(ABC):
    def _to_binary_node(self) -> BinaryNode:
        return BinaryNode(self._op, self._lhs, self._rhs)

    def __init__(self, lhs, op, rhs) -> None:
        self._lhs = lhs
        self._op = op
        self._rhs = rhs

    @property
    def _operator(self) -> Operators:
        return self._op

    def evaluate(self) -> float:
        return self._evaluate(self._operator)

    @abstractmethod
    def _evaluate(self, op) -> float:
        pass

    def __and__(self, other: 'ConditionalExpression') -> 'ConditionalExpression':
        if not isinstance(other, ConditionalExpression):
            raise NotImplementedError("need to be implemented 1")
        if self == other:
            return self

        if self.__class__ == ConditionalWithValue and other.__class__ == ConditionalWithValue:
            if other._operator == Operators.EQ:
                if self._operator == Operators.EQ:
                    return ValueWithValue(self._rhs, Operators.EQ, other._rhs)
                else:
                    raise ValueError("need to be implemented 2")
            else:
                if other._operator == Operators.GT:
                    if self._rhs <= other._rhs:
                        return DummyEvaluate(0)
                    return ExpressionWithExpression(self, self._operator, other)
                raise ValueError("need to be implemented 3")

        raise ValueError("need to be implemented 4")

    def __or__(self, other):
        return AccumulationExpression.from_raw(self, Operators.GIVEN, other)

    def __ror__(self, other):
        return AccumulationExpression.from_raw(other, Operators.GIVEN, self)

    def __bool__(self):
        return False

    def __eq__(self, other: 'ConditionalExpression') -> bool:
        if not isinstance(other, ConditionalExpression):
            raise TypeError(
                f"Cant compare equality between {self.__class__.__qualname__} and non ConditionalExpression")
        return self._lhs == other._lhs and self._rhs == other._rhs and self._operator == other._operator

    def __hash__(self):
        return hash((self._lhs, self._operator, self._rhs))

    @staticmethod
    def _create_operator(op: Operators, reverse: bool = False):
        def inned(self: 'ConditionalExpression', other: Any):
            lhs, rhs = self._to_binary_node(), other
            if isinstance(rhs, ConditionalExpression):
                rhs = rhs._to_binary_node()
            else:
                rhs = BinaryNode(rhs)
            if reverse:
                lhs, rhs = rhs, lhs
            return AccumulationExpression(lhs, op, rhs)

        return inned

    __lt__ = _create_operator(Operators.LT)
    __le__ = _create_operator(Operators.LE)
    __gt__ = _create_operator(Operators.GT, reverse=True)
    __ge__ = _create_operator(Operators.GE, reverse=True)


class ValueWithValue(ConditionalExpression):
    def _evaluate(self, op) -> float:
        return int(self._lhs == self._rhs)


class DummyEvaluate(ConditionalExpression):
    def _evaluate(self, op) -> float:
        return self._lhs

    def __init__(self, v: float) -> None:
        super().__init__(v, None, None)


class ConditionalWithValue(ConditionalExpression):
    @property
    def X(self) -> ConditionalVariable:
        return self._lhs

    @property
    def n(self) -> float:
        return self._rhs

    def _evaluate(self, op):
        return self.X.evaluate(op, self.n)


class ConditionalWithConditional(ConditionalExpression):
    @property
    def X(self) -> ConditionalVariable:
        return self._lhs

    @property
    def Y(self) -> ConditionalVariable:
        return self._rhs

    def _evaluate(self, op):
        supp = self.X.supp.intersect(self.Y.supp)
        res = 0.0
        for n in supp:
            res += P(self.X == n) * P(self.Y == n)

        return res


class ExpressionWithExpression(ConditionalExpression):

    def _evaluate(self, op) -> float:
        return self._lhs.evaluate() / self._rhs.evaluate()


__all__ = [
    "ConditionalExpression",
    "ConditionalWithValue",
    "ConditionalWithConditional"
]
