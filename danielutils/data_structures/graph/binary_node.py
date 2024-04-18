from __future__ import annotations
from typing import Optional, TypeVar
from .multinode import MultiNode
from ...metaclasses import ImplicitDataDeleterMeta

T = TypeVar("T")


class BinaryNode(MultiNode[T], metaclass=ImplicitDataDeleterMeta):
    """A 'classic' node class with only one child
    """

    def __init__(self, data: T, l: Optional[BinaryNode[T]] = None,
                 r: Optional[BinaryNode[T]] = None):  # pylint: disable=redefined-builtin
        # intentionally can be None
        super().__init__(data, [l, r])  # type:ignore

    def __str__(self):
        return MultiNode.__str__(self).replace(
            self.__class__.__mro__[1].__name__,
            self.__class__.__name__
        ).replace("[", "").replace("]", "")

    def __repr__(self):
        return str(self)

    def __reversed__(self) -> 'BinaryNode[T]':
        return self.reverse()

    def __eq__(self, other):
        return MultiNode.__eq__(self, other)

    def __iter__(self):
        return MultiNode.__iter__(self)

    @property
    def left(self) -> "BinaryNode[T]":
        """return the next node after self
        """
        return self._children[0]  # type:ignore

    @left.setter
    def left(self, value: "BinaryNode[T]") -> None:
        self._children[0] = value

    @property
    def right(self) -> "BinaryNode[T]":
        """return the next node after self
        """
        return self._children[1]  # type:ignore

    @right.setter
    def right(self, value: "BinaryNode[T]") -> None:
        self._children[1] = value

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def reverse(self) -> 'BinaryNode[T]':
        new_left = self.right.reverse() if self.right is not None else None
        new_right = self.left.reverse() if self.left is not None else None
        return BinaryNode(self.data, new_left, new_right)

    def depth(self) -> int:
        return MultiNode.depth(self)


__all__ = [
    "BinaryNode"
]
