from fractions import Fraction
from typing import Callable, Any
from ..protocols import Evaluable
from ..operator import Operator
from ....data_structures import BinarySyntaxTree as BST


class AccumulationExpression(Evaluable):
    @classmethod
    def from_raw(cls, lhs: Any, op: Operator, rhs: Any):
        return cls(BST.Node(lhs), op, BST.Node(rhs))

    def __init__(self, lhs: BST.Node, op: Operator, rhs: BST.Node) -> None:
        root = BST.Node(
            op,
            lhs,
            rhs
        )
        self._tree = BST(root)

    @staticmethod
    def _create_operator(op) -> Callable[['AccumulationExpression', Any], 'AccumulationExpression']:
        def operator(self, other) -> 'AccumulationExpression':
            self._add_right(other, op)
            return self

        return operator

    __eq__ = _create_operator(Operator.EQ)
    __ne__ = _create_operator(Operator.NE)
    __gt__ = _create_operator(Operator.GT)
    __ge__ = _create_operator(Operator.GE)
    __lt__ = _create_operator(Operator.LT)
    __le__ = _create_operator(Operator.LE)

    def _add_right(self, right, op) -> None:
        replacement = BST.Node(
            op,
            BST.Node(self._tree.bottom_right.data),
            BST.Node(right)
        )
        self._tree.bottom_right = replacement

    def add_left(self, left, op) -> None:
        replacement = BST.Node(
            op,
            BST.Node(left),
            BST.Node(self._tree.bottom_left.data),
        )
        self._tree.bottom_left = replacement

    def evaluate(self) -> Fraction:
        return self._tree.evaluate({
            Operator.GIVEN: lambda lhs, rhs: (lhs & rhs).evaluate | rhs.evaluate(),
            Operator.AND: lambda lhs, rhs: (lhs & rhs).evaluate,
            Operator.EQ: lambda lhs, rhs: lhs == rhs,
            Operator.GE: lambda lhs, rhs: lhs >= rhs,
            Operator.GT: lambda lhs, rhs: lhs > rhs,
            Operator.LE: lambda lhs, rhs: lhs <= rhs,
            Operator.LT: lambda lhs, rhs: lhs < rhs,
            Operator.NE: lambda lhs, rhs: lhs != rhs,
        })


__all__ = [
    'AccumulationExpression'
]
