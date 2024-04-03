from abc import ABC, abstractmethod
from ..funcs import ProbabilityFunction as P
from ..conditional_variable import ConditionalVariable
from ..accumulation_expression import AccumulationExpression
from ..operators import Operators


class ConditionalExpression(ABC):
    def __init__(self, lhs, op, rhs) -> None:
        self._lhs = lhs
        self._op = op
        self._rhs = rhs

    @property
    def operator(self) -> Operators:
        return self._op

    def evaluate(self) -> float:
        return self._evaluate(self.operator)

    @abstractmethod
    def _evaluate(self, op) -> float:
        pass

    def __and__(self, other):
        if not isinstance(other, ConditionalExpression):
            raise NotImplementedError("need to be implemented")

        if self.__class__ == ConditionalWithValue and other.__class__ == ConditionalWithValue:
            if self._lhs is other._lhs:
                if self.operator == other.operator == Operators.EQ:
                    return ValueWithValue(self._rhs, Operators.EQ, other._rhs)


        pass
        #         if self.operator
        #         else:
        #             pass
        #         if self._rhs >= other._rhs:
        #             return self.evaluate() / other.evaluate()
        #         return 0
        # if self.__class__ == ConditionalWithConditional and other.__class__ == ConditionalWithConditional:
        #     pass
        # else:
        #     pass

    def __or__(self, other):
        return AccumulationExpression(self, Operators.GIVEN, other)

    def __ror__(self, other):
        return AccumulationExpression(other, Operators.GIVEN, self)


class ValueWithValue(ConditionalExpression):
    def _evaluate(self, op) -> float:
        return int(self._lhs == self._rhs)


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


__all__ = [
    "ConditionalExpression",
    "ConditionalWithValue",
    "ConditionalWithConditional"
]
