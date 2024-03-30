from abc import ABC, abstractmethod
from ..funcs import P
from ..conditional_variable import ConditionalVariable
from ..accumulation_expression import AccumulationExpression


class ConditionalExpression(ABC):
    def __init__(self, lhs, rhs) -> None:
        self._lhs = lhs
        self._rhs = rhs

    def evaluate(self) -> float:
        return self._evaluate()

    @abstractmethod
    def _evaluate(self) -> float:
        pass

    def __and__(self, other):
        # TODO
        pass

    def __or__(self, other):
        return AccumulationExpression(self, AccumulationExpression.Operators.GIVEN, other)

    def __ror__(self, other):
        return AccumulationExpression(other, AccumulationExpression.Operators.GIVEN, self)


class ConditionalWithValue(ConditionalExpression):
    @property
    def X(self) -> ConditionalVariable:
        return self._lhs

    @property
    def n(self) -> float:
        return self._rhs

    def _evaluate(self):
        return self.X.evaluate(self.n)


class ConditionalWithConditional(ConditionalExpression):
    @property
    def X(self) -> ConditionalVariable:
        return self._lhs

    @property
    def Y(self) -> ConditionalVariable:
        return self._rhs

    def _evaluate(self):
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
