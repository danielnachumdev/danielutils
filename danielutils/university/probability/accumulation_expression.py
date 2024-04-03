from enum import Enum
from typing import Any
from ...data_structures import BST, BinaryNode
from .operators import Operators


class AccumulationExpression:
    def __init__(self, lhs: Any, op: Operators, rhs: Any) -> None:
        root = BinaryNode(
            op,
            BinaryNode(lhs),
            BinaryNode(rhs)
        )
        self.tree = BST(root)

    def __eq__(self, other):
        self.add_right(other, Operators.EQ)
        return self

    def __ge__(self, other):
        self.add_right(other, Operators.GE)
        return self

    def __gt__(self, other):
        self.add_right(other, Operators.GT)
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
    def _handle_greater_equals(lhs: Any, rhs: Any):
        return lhs.data >= rhs.data

    @staticmethod
    def _handle_greater_than(lhs: Any, rhs: Any):
        pass

    @staticmethod
    def _handle_less_equals(lhs: Any, rhs: Any):
        pass

    @staticmethod
    def _handle_less_than(lhs: Any, rhs: Any):
        pass

    @staticmethod
    def _handle_not_equals(lhs: Any, rhs: Any):
        pass

    @staticmethod
    def _handle_given(lhs: Any, rhs: Any):
        return (lhs & rhs).evaluate() / rhs.evaluate()

    def evaluate(self):
        return self.tree.evaluate({
            Operators.EQ: AccumulationExpression._handle_equals,
            Operators.GIVEN: AccumulationExpression._handle_given,
            Operators.GE: AccumulationExpression._handle_greater_equals,
            Operators.GT: AccumulationExpression._handle_greater_than,
            Operators.LE: AccumulationExpression._handle_less_equals,
            Operators.LT: AccumulationExpression._handle_less_than,
            Operators.NE: AccumulationExpression._handle_not_equals,
        })


__all__ = [
    'AccumulationExpression'
]
