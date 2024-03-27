from typing import Optional, Generator, List as t_list, Set as t_set
from .queue import Queue
from .node import MultiNode
from ..reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as t_list, set as t_set


class Graph:
    """A general-purpose Graph class.

    This class represents a directed graph, where nodes can be connected through edges.

    Attributes:
        nodes (Optional[t_list[MultiNode]]): A list of MultiNode instances representing the nodes in the graph.
                                             Default is an empty list.

    Methods:
        __init__(self, nodes: Optional[t_list[MultiNode]] = None): Initialize the Graph with given nodes.
        add_node(self, node): Add a node to the graph.
        _extended_dfs(self) -> Generator: Perform an extended depth-first search on the graph.
        dfs(self) -> Generator: Perform a depth-first search on the graph.
        topological_sort(self) -> list: Get a topological sort of the graph nodes.
        bfs(self) -> Generator: Perform a breadth-first search on the graph.
        __str__(self) -> str: Get a string representation of the graph.

    """

    def __init__(self, nodes: Optional[t_list[MultiNode]] = None):
        self.nodes: t_list[MultiNode] = nodes if nodes is not None else []

    def add_node(self, node)->None:
        """Add a node to the graph.

        Args:
            node: The MultiNode instance to add to the graph.
        """
        self.nodes.append(node)

    def _extended_dfs(self) -> Generator[MultiNode, None, list[MultiNode]]:
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
        all_nodes: list[MultiNode] = []

        def handle_node(node: MultiNode) -> Generator[MultiNode, None, None]:
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


    def dfs(self) -> Generator:
        """Perform a depth-first search on the graph.

        This method performs a depth-first search (DFS) on the graph using the private _extended_dfs method.

        Yields:
            Generator: The MultiNode instances in the order of depth-first traversal.
        """
        yield from self._extended_dfs()

    def topological_sort(self) -> list[MultiNode]:
        """Get a topological sort of the graph nodes.

        This method performs a topological sort on the graph using the private _extended_dfs method.

        Returns:
            list: A list containing the MultiNode instances in topological order.
        """
        g = self._extended_dfs()
        try:
            while True:
                next(g)
        except StopIteration as e:
            return e.value

    def bfs(self) -> Generator:
        """Perform a breadth-first search on the graph.

        This method performs a breadth-first search (BFS) on the graph using a queue.

        Yields:
            Generator: The MultiNode instances in the order of breadth-first traversal.
        """
        q = Queue()
        for node in self.nodes:
            q.push(node)
        seen: t_set[MultiNode] = set()
        for node in q:
            if node not in seen:
                seen.add(node)
                yield node
                for child in node._children:  # pylint: disable=protected-access
                    q.push(child)

    def __str__(self) -> str:
        tmp = []
        for n in self.dfs():
            tmp.append(f"\t{str(n)}")
        return "Graph(\n" + ",\n".join(tmp) + "\n)"

    def __iter__(self):
        return iter(self.nodes)


__all__ = [
    "Graph"
]
