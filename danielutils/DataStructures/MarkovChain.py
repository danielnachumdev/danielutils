from ..Decorators import validate_explicit, overload
from ..Typing import Any, Iterable, Union
import random
INDEX_INDEX = 0
OCCUPANCE_INDEX = 1


class MarkovNode:
    @overload(None, Any)
    def __init__(self, value: Any) -> None:
        self.value = value
        self.occurrences = []
        self.indices = []

    @overload(None, Any, list[tuple[int, int]])
    def __init__(self, value: Any, children: list[tuple[float, int]] = None) -> None:
        self.value = value
        self.occurrences = [tup[OCCUPANCE_INDEX] for tup in children]
        self.indices = [tup[INDEX_INDEX] for tup in children]

    @overload(None, Any, list[int], list[int])
    def __init__(self, value: Any,  indices: list[int], occurrences: list[int]) -> None:
        if len(occurrences) != len(indices):
            raise ValueError("")
        self.value = value
        self.occurrences = occurrences
        self.indices = indices

    def __str__(self) -> str:
        return f"({str(self.value)})"

    def add_child(self, occurrence: float, index: int) -> None:
        self.occurrences.append(occurrence)
        self.indices.append(index)

    def next(self) -> int:
        count = sum(self.occurrences)
        selector = random.randint(0, count)
        for i, child_occur in enumerate(self.occurrences):
            selector -= child_occur
            if selector <= 0:
                break
        return self.indices[i]

    def __repr__(self) -> str:
        return str(self)

    def has_children(self) -> bool:
        return len(self.occurrences) > 0


class MarkovChain:
    @validate_explicit(None, list[MarkovNode])
    def __init__(self, nodes: list[MarkovNode] = None) -> None:
        self.nodes = nodes if nodes is not None else []

    @validate_explicit(None, int)
    def __getitem__(self, index: int) -> MarkovNode:
        return self.nodes[index]

    @validate_explicit(None, MarkovNode)
    def append(self, node: MarkovNode) -> None:
        self.nodes.append(node)

    def __iter__(self) -> Iterable:
        return iter(self.nodes)

    def __str__(self) -> str:
        return " -> ".join([str(node) for node in self])

    def __len__(self) -> int:
        return len(self.nodes)

    def generate_sequence(self, max_length: int) -> list[MarkovNode]:
        res = []
        index = 0
        for _ in range(max_length):
            n = self[index]
            res.append(n)
            if not n.has_children():
                break
            index = n.next()
        return res


__all__ = [
    "MarkovNode",
    "MarkovChain"
]
