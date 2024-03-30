from __future__ import annotations
from typing import Optional, TypeVar
from ...metaclasses import ImplicitDataDeleterMeta
from .multinode import MultiNode

T = TypeVar("T")


class BinaryNode(MultiNode[T], metaclass=ImplicitDataDeleterMeta):
    """A 'classic' node class with only one child
    """

    def __init__(self, data: T, l: Optional[BinaryNode[T]] = None,
                 r: Optional[BinaryNode[T]] = None):  # pylint: disable=redefined-builtin
        super().__init__(data, [l, r])

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

    def __str__(self):
        return MultiNode.__str__(self).replace(
            self.__class__.__mro__[1].__name__,
            self.__class__.__name__
        ).replace("[", "").replace("]", "")

    def __repr__(self):
        return str(self)


__all__ = [
    "BinaryNode"
]
