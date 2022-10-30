from __future__ import annotations
from ..Typing import Any, Sequence, Union, Tuple, TypeVar
from ..Decorators import overload, validate


class GraphNode:
    def __init__(self, value: Any):
        self.value = value

    def __str__(self) -> str:
        return f"GN(V={self.value})"

    def __repr__(self) -> str:
        return str(self)


class Connection:
    @validate(None, GraphNode, GraphNode, Any)
    def __init__(self, node1: GraphNode, node2: GraphNode, weight: Any):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight


class Graph:
    @classmethod
    @validate(None, list, list, list)
    def from_lists(cls, values: list[Any], connections: list[list[int]]) -> Graph:
        nodes = [GraphNode(v) for v in values]
        parsed_connections = []
        for i1, i_connections in enumerate(connections):
            for i2 in i_connections:
                parsed_connections.append(Connection(nodes[i1], nodes[i2]))
        return cls(
            nodes,
            parsed_connections,
        )

    def __init__(self, nodes: list[GraphNode], connections: list[Connection]):
        if not (len(nodes) == len(connections)):
            raise ValueError("Length of input params is not th same")
        self.nodes = nodes
        self.connections = connections

    def __str__(self) -> str:
        res = ", ".join([
            f"({value},{connections},{weights})" for value, connections, weights in self
        ])
        return res

    def __len__(self) -> int:
        return len(self.nodes)

    def __iter__(self):
        for i in range(len(self)):
            yield (self.nodes[i], self.connections[i], self.weights[i]if self.weights is not None else None)

    @overload(None, GraphNode)
    def __contains__(self, node: GraphNode) -> bool:
        return node in self.nodes

    @overload(None, Connection)
    def __contains__(self, connection: Connection) -> bool:
        return connection in self.connections

    def clone() -> Graph:
        pass


class TypedGraph(Graph):
    def __init__(self, nodes: list[GraphNode], connections: list[list[int]], weights: list[list[Any]] = None) -> None:
        for i in range(1, len(nodes)):
            if type(nodes[0].value) != type(nodes[i].value):
                raise TypeError(
                    "One or more of the values is of different type than the others")
        super().__init__(nodes, connections, weights)


__all__ = [
    "Graph",
    "TypedGraph"
]
