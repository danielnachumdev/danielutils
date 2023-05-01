from .Queue import Queue
from .Node import MultiNode


class Graph:
    def __init__(self, nodes: list[MultiNode] = None):
        self.nodes: list[MultiNode] = nodes if nodes is not None else []

    def add_node(self, node):
        self.nodes.append(node)

    def _extended_dfs(self):
        seen = set()
        enter_times = dict()
        exit_times = dict()
        travel_index = 1
        all_nodes = []

        def handle_node(node: MultiNode):
            nonlocal travel_index
            seen.add(node)
            all_nodes.append(node)
            yield node
            for node in node._children:
                if node not in seen:
                    travel_index += 1
                    enter_times[node] = travel_index
                    if node is not None:
                        yield from handle_node(node)
                    travel_index += 1
                    exit_times[node] = travel_index

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

    def dfs(self):
        yield from self._extended_dfs()

    def topological_sort(self):
        g = self._extended_dfs()
        try:
            while True:
                next(g)
        except StopIteration as e:
            return e.value

    def bfs(self):
        q = Queue()
        for node in self.nodes:
            q.push(node)
        seen = set()
        for node in q:
            if node not in seen:
                seen.add(node)
                yield node
                for child in node._children:
                    q.push(child)

    def __str__(self) -> str:
        tmp = []
        for n in self.dfs():
            tmp.append(f"\t{str(n)}")
        return "Graph(\n"+",\n".join(tmp)+"\n)"


__all__ = [
    "Graph"
]
