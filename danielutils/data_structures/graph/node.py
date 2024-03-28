from __future__ import annotations
from typing import Optional, TypeVar
from ...metaclasses import ImplicitDataDeleterMeta
from .multinode import MultiNode

T = TypeVar("T")


class Node(MultiNode[T], metaclass=ImplicitDataDeleterMeta):
    """A 'classic' node class with only one child
    """

    def __init__(self, data: T, next: Optional[Node[T]] = None):  # pylint: disable=redefined-builtin
        super().__init__(data, [next])

    @property
    def next(self) -> "Node[T]":
        """return the next node after self
        """
        return self._children[0]  # type:ignore

    @next.setter
    def next(self, value: Node[T]) -> None:
        self._children[0] = value

    def __str__(self):
        # res = ""
        # seen = set()

        # def handle_node(node: Node):
        #     nonlocal res
        #     if node in seen:
        #         res += "..."
        #     else:
        #         seen.add(node)
        #         res += f"Node({node.data}, "
        #         if node.next is None:
        #             res += "None)"
        #         elif node.next in seen:
        #             res += "...)"

        # curr = self
        # while curr is not None:
        #     handle_node(curr)
        #     curr = curr.next
        #     if curr in seen:
        #         break
        # return res+")"
        return MultiNode.__str__(self).replace(
            self.__class__.__mro__[1].__name__,
            self.__class__.__name__
        ).replace("[", "").replace("]", "")

    def __repr__(self):
        return str(self)


__all__ = [
    "Node"
]
