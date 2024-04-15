from .evaluable import Evaluable
from typing import Any
from data_structures import BinarySyntaxTree, BinaryNode
from .operators import Operators


def _handle_equals(lhs: Any, rhs: Any):
    return lhs.data == rhs.data


def _handle_greater_equals(lhs: Any, rhs: Any):
    return lhs.data >= rhs.data


def _handle_greater_than(lhs: Any, rhs: Any):
    return lhs.data > rhs.data


def _handle_less_equals(lhs: Any, rhs: Any):
    return lhs.data <= rhs.data


def _handle_less_than(lhs: Any, rhs: Any):
    return lhs.data < rhs.data


def _handle_not_equals(lhs: Any, rhs: Any):
    return lhs.data != rhs.data


def _handle_given(lhs: Any, rhs: Any):
    return _handle_and(lhs, rhs) / rhs.evaluate()


def _handle_and(lhs: Any, rhs: Any):
    return (lhs & rhs).evaluate()


class AccumulationExpression(Evaluable):
    @classmethod
    def from_raw(cls, lhs: Any, op: Operators, rhs: Any):
        return cls(BinaryNode(lhs), op, BinaryNode(rhs))

    def __init__(self, lhs: BinaryNode, op: Operators, rhs: BinaryNode) -> None:
        root = BinaryNode(
            op,
            lhs,
            rhs
        )
        self.tree = BinarySyntaxTree(root)

    def __eq__(self, other):
        self.add_right(other, Operators.EQ)
        return self

    def __ne__(self, other):
        self.add_right(other, Operators.EQ)
        return self

    def __ge__(self, other):
        self.add_right(other, Operators.GE)
        return self

    def __gt__(self, other):
        self.add_right(other, Operators.GT)
        return self

    def __lt__(self, other):
        self.add_right(other, Operators.GT)
        return self

    def __le__(self, other):
        self.add_right(other, Operators.GT)
        return self

    def add_right(self, right, op) -> None:
        replacement = BinaryNode(
            op,
            BinaryNode(self.tree.bottom_right.data),
            BinaryNode(right)
        )
        self.tree.bottom_right = replacement

    def add_left(self, left, op) -> None:
        replacement = BinaryNode(
            op,
            BinaryNode(left),
            BinaryNode(self.tree.bottom_left.data),
        )
        self.tree.bottom_left = replacement

    def evaluate(self):
        return self.tree.evaluate({
            Operators.GIVEN: _handle_given,
            Operators.AND: _handle_and,
            Operators.EQ: _handle_equals,
            Operators.GE: _handle_greater_equals,
            Operators.GT: _handle_greater_than,
            Operators.LE: _handle_less_equals,
            Operators.LT: _handle_less_than,
            Operators.NE: _handle_not_equals,
        })


__all__ = [
    'AccumulationExpression'
]