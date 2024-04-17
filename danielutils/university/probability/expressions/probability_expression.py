from typing import Any, Callable
from ..protocols import Evaluable
from ..operator import Operator
from fractions import Fraction
from .accumulation_expression import AccumulationExpression
from ....data_structures import BinarySyntaxTree as BST


class ProbabilityExpression(Evaluable):
    OPERATOR_TYPE = Callable[['ProbabilityExpression', Any], 'AccumulationExpression']

    def _to_binary_node(self) -> BST.Node:
        return BST.Node(self.op, self.lhs, self.rhs)

    def __init__(self, lhs: Evaluable, op: Operator, rhs: Any):
        self._lhs = lhs
        self._op = op
        self._rhs = rhs

    @staticmethod
    def _create_operator(op: Operator, reverse: bool = False):
        def operator(self: 'ProbabilityExpression', other: Any):
            lhs, rhs = self._to_binary_node(), other
            if isinstance(rhs, ProbabilityExpression):
                rhs = rhs._to_binary_node()
            else:
                rhs = BST.Node(rhs)
            if reverse:
                lhs, rhs = rhs, lhs
            return AccumulationExpression(lhs, op, rhs)

        return operator

    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)
    __or__: OPERATOR_TYPE = _create_operator(Operator.GIVEN)
    __ror__: OPERATOR_TYPE = _create_operator(Operator.GIVEN, reverse=True)

    def __and__(self, other: 'ProbabilityExpression') -> 'ProbabilityExpression':
        pass

    def __eq__(self, other: 'ProbabilityExpression') -> bool:
        if not isinstance(other, ProbabilityExpression):
            raise TypeError(
                f"Cant compare equality between {self.__class__.__qualname__} and non ConditionalExpression")
        return self.lhs == other.lhs and self.rhs == other.rhs and self.op == other.op

    def __hash__(self) -> int:
        return hash((self.__class__, self.lhs, self.op, self.rhs))

    def evaluate(self) -> Fraction:
        return self.lhs.evaluate(self.rhs, self.op)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.lhs} {self.op.value} {self.rhs})"

    @property
    def inverse(self) -> 'ProbabilityExpression':
        return ProbabilityExpression(self.lhs, self.op.inverse, self.rhs)

    @property
    def lhs(self):
        return self._lhs

    @property
    def op(self):
        return self._op

    @property
    def rhs(self):
        return self._rhs


__all__ = [
    'ProbabilityExpression',
]
