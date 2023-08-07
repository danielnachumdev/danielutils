from __future__ import annotations
from typing import Any, Optional, Generator
from ..MetaClasses import ImplicitDataDeleterMeta


class MultiNode:
    """A node class with no limit to children amount
    """

    def __init__(self, data: Any, children: Optional[list[Optional[MultiNode]]] = None):
        self.data = data
        self._children = children if children is not None else []

    def __getitem__(self, index) -> Any:
        return self._children[index]

    def __setitem__(self, value, index) -> None:
        self._children[index] = value

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self) -> Generator:
        yield from self._children

    def __str__(self) -> str:
        res = ""
        seen = set()

        def handle_node(node: MultiNode):
            nonlocal res
            # res += f"MultiNode({node.data}, ["
            seen.add(node)
            tmp = []
            for child in node._children:  # pylint: disable=protected-access
                if child in seen:
                    tmp.append("...")
                else:
                    if child is not None:
                        tmp.append(handle_node(child))
            return f"{node.__class__.__name__}({node.data}, ["+", ".join(tmp)+"])"

        return handle_node(self)

    def __repr__(self):
        return str(self)

    def add_child(self, child):
        """adds a child to current node
        """
        self._children.append(child)


class Node(MultiNode, metaclass=ImplicitDataDeleterMeta):
    """A 'classic' node class with only one child
    """

    def __init__(self, data, next: Optional[Node] = None):  # pylint: disable=redefined-builtin
        super().__init__(data, [next])

    @property
    def next(self):
        """return the next node after self
        """
        return self._children[0]

    @next.setter
    def next(self, value):
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
    "MultiNode",
    "Node"
]
