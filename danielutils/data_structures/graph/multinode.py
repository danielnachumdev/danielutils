from typing import  Optional, Generator, TypeVar, Generic

T = TypeVar("T")


class MultiNode(Generic[T]):
    """A node class with no limit to children amount
    """

    def __init__(self, data: T, children: Optional[list[Optional["MultiNode[T]"]]] = None):
        self.data: T = data
        self._children: list[MultiNode[T]] = children if children is not None else []

    def __getitem__(self, index) -> T:
        return self._children[index]

    def __setitem__(self, value: T, index: int) -> None:
        self._children[index] = value

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
            return f"{node.__class__.__name__}({node.data}, [" + ", ".join(tmp) + "])"

        return handle_node(self)

    def __repr__(self):
        return str(self)

    def add_child(self, child: "MultiNode[T]") -> None:
        """adds a child to current node
        """
        self._children.append(child)


__all__ = [
    "MultiNode"
]
