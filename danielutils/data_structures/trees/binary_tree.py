from ..graph import BinaryNode
from typing import TypeVar, Generic

T = TypeVar("T")


class BinaryTree(Generic[T]):
    def __init__(self, root: BinaryNode[T]):
        self._root = root

    @property
    def root(self)->BinaryNode[T]:
        return self._root


__all__ = [
    'BinaryTree'
]
