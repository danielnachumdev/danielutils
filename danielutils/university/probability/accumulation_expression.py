from enum import Enum
from typing import Any
from ...data_structures import BST, BinaryNode


class AccumulationExpression:
    class Operators(Enum):
        GIVEN = "|"
        EQUALS = "=="

    def __init__(self, lhs: Any, op: Operators, rhs: Any) -> None:
        root = BinaryNode(
            op,
            BinaryNode(lhs),
            BinaryNode(rhs)
        )
        self.tree = BST(root)

    def __eq__(self, other):
        self.add_right(other, AccumulationExpression.Operators.EQUALS)
        return self

    def add_right(self, right, op) -> None:
        replacement = BinaryNode(
            op,
            BinaryNode(self.tree.right.data),
            BinaryNode(right)
        )
        self.tree.right = replacement

    def add_left(self, left, op) -> None:
        replacement = BinaryNode(
            op,
            BinaryNode(left),
            BinaryNode(self.tree.left.data),
        )
        self.tree.left = replacement

    @staticmethod
    def _handle_equals(lhs: Any, rhs: Any):
        return lhs.data == rhs.data

    @staticmethod
    def _handle_given(lhs: Any, rhs: Any):
        return (lhs & rhs).evaluate() / rhs.evaluate()

    def evaluate(self):
        return self.tree.evaluate({
            AccumulationExpression.Operators.EQUALS: AccumulationExpression._handle_equals,
            AccumulationExpression.Operators.GIVEN: AccumulationExpression._handle_given,
        })


__all__ = [
    'AccumulationExpression'
]
