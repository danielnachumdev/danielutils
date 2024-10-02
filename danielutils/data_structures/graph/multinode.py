from typing import Optional, Generator, TypeVar, Generic, List as List, Set

from ...reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as List
T = TypeVar("T")


class MultiNode(Generic[T]):
    """A node class with no limit to children amount
    """

    def __init__(self, data: T, children: Optional[List[Optional['MultiNode[T]']]] = None):
        self.data: T = data
        self._children: List[Optional[MultiNode[T]]] = children if children is not None else []

    def __getitem__(self, index) -> T:
        return self._children[index]

    def __setitem__(self, value: T, index: int) -> None:
        self._children[index] = value  # type:ignore

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self) -> Generator["MultiNode[T]", None, None]:
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
            child_str = ", [" + ", ".join(tmp) + "]" if len(tmp) > 0 else ""
            return f"{node.__class__.__name__}({node.data}{child_str})"

        return handle_node(self)

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, MultiNode):
            return False

        return self.data == other.data and len(self) == len(other) and all(
            [a.data == b.data for a, b in zip(self, other)])

    def __hash__(self) -> int:
        return hash((self.__class__, self.data, len(self), (c.data for c in self)))

    def __reversed__(self) -> 'MultiNode[T]':
        return self.reverse()

    @property
    def is_leaf(self) -> bool:
        return len(self._children) == 0

    def reverse(self) -> 'MultiNode[T]':
        return MultiNode(self.data, self._children[::-1])

    def add_child(self, child: "MultiNode[T]") -> None:
        """adds a child to current node
        """
        self._children.append(child)

    def depth(self) -> int:
        """
        Returns the depth of the current node (including).
        Returns:
            int
        """

        def helper(cur: MultiNode, seen: Optional[Set[MultiNode]] = None) -> int:
            if not isinstance(cur, MultiNode):
                return 0
            if seen is None:
                seen = set()
            elif cur in seen:
                return 0
            seen.add(cur)
            seq = [helper(child, seen) for child in cur if ((child is not None) and (child not in seen))]
            return 1 + (max(seq) if len(seq) > 0 else 0)

        return helper(self)


__all__ = [
    "MultiNode"
]
