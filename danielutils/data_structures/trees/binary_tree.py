from enum import Enum

from ..graph import BinaryNode
from typing import TypeVar, Generic, Iterator

T = TypeVar("T")


class BinaryTree(Generic[T]):
    Node = BinaryNode

    class TraversalMode(Enum):
        First = 1
        Middle = 2
        Last = 3

    def __init__(self, root: BinaryNode[T]):
        self._root = root

    def __reversed__(self) -> 'BinaryTree[T]':
        return self.reverse()

    def __iter__(self) -> Iterator[BinaryNode[T]]:
        yield from self.traverse(BinaryTree.TraversalMode.First)

    def __eq__(self, other):
        if not isinstance(other, BinaryTree):
            return False

        for a, b in zip(self, other):
            if not (a == b):
                return False
        return True

    @property
    def root(self) -> BinaryNode[T]:
        return self._root

    def traverse(self, mode: 'TraversalMode') -> Iterator[BinaryNode[T]]:
        def helper(node: BinaryNode[T]):
            if mode == self.TraversalMode.First:
                yield node
            if node.left is not None:
                yield from helper(node.left)
            if mode == self.TraversalMode.Middle:
                yield node
            if node.right is not None:
                yield from helper(node.right)
            if mode == self.TraversalMode.Last:
                yield node

        yield from helper(self._root)

    def reverse(self) -> "BinaryTree[T]":
        return BinaryTree(self.root.reverse())

    def depth(self) -> int:
        return self.root.depth()

__all__ = [
    'BinaryTree'
]
