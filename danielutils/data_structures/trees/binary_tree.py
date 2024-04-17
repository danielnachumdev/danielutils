from ..graph import BinaryNode
from typing import TypeVar, Generic, Iterator

T = TypeVar("T")


class BinaryTree(Generic[T]):
    def __init__(self, root: BinaryNode[T]):
        self._root = root

    @property
    def root(self) -> BinaryNode[T]:
        return self._root

    def __iter__(self) -> Iterator[BinaryNode[T]]:
        def helper(node: BinaryNode[T]):
            yield node
            if node.left is not None:
                yield from helper(node.left)
            if node.right is not None:
                yield from helper(node.right)

        yield from helper(self._root)

    def __eq__(self, other):
        if not isinstance(other, BinaryTree):
            return False

        for a, b in zip(self, other):
            if not (a == b):
                return False
        return True


__all__ = [
    'BinaryTree'
]
