from .Queue import Queue
from .Node import MultiNode


class Graph:
    def __init__(self, nodes: list[MultiNode] = None):
        self.nodes: list[MultiNode] = nodes if nodes is not None else []

    def add_node(self, node):
        self.nodes.append(node)

    def dfs(self):
        seen = set()

        def handle_node(node: MultiNode):
            seen.add(node)
            yield node
            for node in node._children:
                if node not in seen:
                    yield from handle_node(node)
        for node in self.nodes:
            if node not in seen:
                yield from handle_node(node)

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
