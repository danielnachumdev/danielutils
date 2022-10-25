from ..Decorators import validate, overload
from ..Typing import Any, Tuple, Iterable, Union
import random

INDEX_INDEX = 0
OCCURANCE_INDEX = 1


class MarkovNode:
    @overload(None, Any)
    def __init__(self, value: Any) -> None:
        self.value = value
        self.occurrences = []
        self.indecies = []

    @overload(None, Any, list[Tuple[int, int]])
    def __init__(self, value: Any, children: list[Tuple[float, int]] = None) -> None:
        self.value = value
        self.occurrences = [tup[OCCURANCE_INDEX] for tup in children]
        self.indecies = [tup[INDEX_INDEX] for tup in children]

    @overload(None, Any, list[int], list[int])
    def __init__(self, value: Any,  indecies: list[int], occurrences: list[int]) -> None:
        if len(occurrences) != len(indecies):
            raise ValueError("")
        self.value = value
        self.occurrences = occurrences
        self.indecies = indecies

    def __str__(self) -> str:
        return f"({str(self.value)})"

    def add_child(self, occurrence: float, index: int) -> None:
        self.occurrences.append(occurrence)
        self.indecies.append(index)

    def select_random_child(self) -> int:
        count = sum(self.occurrences)
        selector = random.randint(0, count)
        for i, child_occur in enumerate(self.occurrences):
            selector -= child_occur
            if selector <= 0:
                break
        return self.indecies[i]

    def __repr__(self) -> str:
        return str(self)

    def has_children(self) -> bool:
        return len(self.occurrences) > 0


class MarkovChain:
    @validate(None, list[MarkovNode])
    def __init__(self, nodes: list[MarkovNode] = None) -> None:
        self.nodes = nodes if nodes is not None else []

    @validate(None, int)
    def __getitem__(self, index: int) -> MarkovNode:
        return self.nodes[index]

    @validate(None, MarkovNode)
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
            index = n.select_random_child()
        return res


__all__ = [
    "MarkovNode",
    "MarkovChain"
]
