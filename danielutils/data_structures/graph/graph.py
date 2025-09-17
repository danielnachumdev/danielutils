import logging
from typing import Optional, Generator, List as List, Set as Set, Dict as Dict, Generic, \
from ..logging_.utils import get_logger
    TypeVar, Iterable, Iterator
from ..queue import Queue
from .multinode import MultiNode
from ...reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as List, set as Set, dict as Dict

T = TypeVar("T")

logger = get_logger(__name__)


class Graph(Generic[T]):
    """A general-purpose Graph class.

    This class represents a directed graph, where nodes can be connected through edges.

    Attributes:
        nodes (Optional[List[MultiNode]]): A list of MultiNode instances representing the nodes in the graph.
                                             Default is an empty list.

    Methods:
        __init__(self, nodes: Optional[List[MultiNode]] = None): Initialize the Graph with given nodes.
        add_node(self, node): Add a node to the graph.
        _extended_dfs(self) -> Generator: Perform an extended depth-first search on the graph.
        dfs(self) -> Generator: Perform a depth-first search on the graph.
        topological_sort(self) -> list: Get a topological sort of the graph nodes.
        bfs(self) -> Generator: Perform a breadth-first search on the graph.
        __str__(self) -> str: Get a string representation of the graph.

    """

    def to_dict(self) -> Dict[T, Set[T]]:
        """
        converts the graph to a dictionary.
        Returns:
            dict: A dictionary representing the graph.
        """
        logger.debug(f"Converting graph with {len(self.nodes)} nodes to dictionary")
        dct: Dict[T, Set[T]] = {}
        for node in self:
            v = dct.get(node.data, set())
            for child in node:
                v.add(child.data)
            dct[node.data] = v
        logger.debug(f"Graph converted to dictionary with {len(dct)} entries")
        return dct

    @staticmethod
    def from_dict(dct: Dict[T, Iterable[T]]) -> "Graph[T]":
        """
        converts a dictionary to a graph.
        Args:
            dct: A dictionary representing the graph.

        Returns:
            Graph[T]: A graph representing the given dictionary.
        """
        logger.debug(f"Creating graph from dictionary with {len(dct)} entries")
        g: Graph[T] = Graph()
        seen: Dict[T, MultiNode[T]] = {}
        for k, v in dct.items():
            seen[k] = seen.get(k, MultiNode(k))

            for o in v:
                seen[o] = seen.get(o, MultiNode(o))
                seen[k].add_child(seen[o])

            g.add_node(seen[k])
        logger.info(f"Graph created from dictionary with {len(g.nodes)} nodes")
        return g

    def __init__(self, nodes: Optional[List[MultiNode[T]]] = None):
        self.nodes: List[MultiNode[T]] = nodes if nodes is not None else []
        logger.debug(f"Graph initialized with {len(self.nodes)} nodes")

    def add_node(self, node: MultiNode[T]) -> None:
        """Add a node to the graph.

        Args:
            node: The MultiNode instance to add to the graph.
        """
        self.nodes.append(node)
        logger.debug(f"Added node to graph, total nodes: {len(self.nodes)}")

    def _extended_dfs(self) -> Generator[MultiNode[T], None, List[MultiNode[T]]]:
        """Perform an extended depth-first search on the graph.

        This private method performs an extended depth-first search (DFS) on the graph,
        keeping track of enter and exit times for each node, and returns a generator that yields
        nodes in the order of DFS traversal.

        Yields:
            Generator: The MultiNode instances in the order of depth-first traversal.
        """
        seen: set = set()
        enter_times: dict = {}
        exit_times: dict = {}
        travel_index: int = 1
        all_nodes: List[MultiNode] = []

        def handle_node(node: MultiNode[T]) -> Generator[MultiNode[T], None, None]:
            nonlocal travel_index
            seen.add(node)
            all_nodes.append(node)
            yield node
            for subnode in node._children:  # pylint: disable=protected-access
                if subnode not in seen:
                    travel_index += 1
                    enter_times[subnode] = travel_index
                    if subnode is not None:
                        yield from handle_node(subnode)
                    travel_index += 1
                    exit_times[subnode] = travel_index

        for node in self.nodes:
            if node not in seen:
                enter_times[node] = travel_index
                travel_index += 1
                yield from handle_node(node)
                travel_index += 1
                exit_times[node] = travel_index
        topological_order = sorted(
            all_nodes, key=lambda v: exit_times[v], reverse=True)
        return topological_order

    # def topological_sort(graph: Graph):
    #     def dfs(node: MultiNode, visited: set, result: list):
    #         visited.add(node)
    #         for neighbor in node:
    #             if neighbor not in visited:
    #                 dfs(neighbor, visited, result)
    #         result.append(node)
    #
    #     visited: set = set()
    #     result: list = []
    #     for node in graph:
    #         if node not in visited:
    #             dfs(node, visited, result)
    #     return result[::-1]  # Reverse the result list

    def dfs(self) -> Generator[MultiNode[T], None, None]:
        """Perform a depth-first search on the graph.

        This method performs a depth-first search (DFS) on the graph using the private _extended_dfs method.

        Yields:
            Generator: The MultiNode instances in the order of depth-first traversal.
        """
        logger.debug(f"Starting DFS traversal on graph with {len(self.nodes)} nodes")
        yield from self._extended_dfs()

    def topological_sort(self) -> List[MultiNode[T]]:
        """Get a topological sort of the graph nodes.

        This method performs a topological sort on the graph using the private _extended_dfs method.

        Returns:
            list: A list containing the MultiNode instances in topological order.
        """
        logger.debug(f"Starting topological sort on graph with {len(self.nodes)} nodes")
        g = self._extended_dfs()
        try:
            while True:
                next(g)
        except StopIteration as e:
            result = e.value
            logger.info(f"Topological sort completed, result has {len(result)} nodes")
            return result

    def bfs(self) -> Generator[MultiNode[T], None, None]:
        """Perform a breadth-first search on the graph.

        This method performs a breadth-first search (BFS) on the graph using a queue.

        Yields:
            Generator: The MultiNode instances in the order of breadth-first traversal.
        """
        logger.debug(f"Starting BFS traversal on graph with {len(self.nodes)} nodes")
        q: Queue[MultiNode[T]] = Queue()
        for node in self.nodes:
            q.push(node)
        seen: Set[MultiNode] = set()
        for node in q:
            if node not in seen:
                seen.add(node)
                yield node
                for child in node._children:  # pylint: disable=protected-access
                    q.push(child)  # type:ignore
        logger.debug(f"BFS traversal completed, visited {len(seen)} nodes")

    def __str__(self) -> str:
        tmp = []
        for n in self.dfs():
            tmp.append(f"\t{str(n)}")
        return "Graph(\n" + ",\n".join(tmp) + "\n)"

    def __iter__(self) -> Iterator[MultiNode[T]]:
        return iter(self.nodes)


__all__ = [
    "Graph"
]
