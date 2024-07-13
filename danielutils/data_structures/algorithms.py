from collections import defaultdict
from typing import TypeVar, List, Callable, Dict
from itertools import product
from copy import deepcopy

NodeT = TypeVar("NodeT")

DistanceMatrix = Dict[NodeT, Dict[NodeT, float]]


def bellman_ford(nodes: List[NodeT], weight_func: Callable[[NodeT, NodeT], float],
                 iteration_callback: Callable[[DistanceMatrix], None],
                 poisoned_reverse: bool = False) -> DistanceMatrix:
    dist: Dict[NodeT, Dict[NodeT, float]] = defaultdict(defaultdict)
    prev: Dict[NodeT, Dict[NodeT, NodeT]] = defaultdict(defaultdict)

    for u, v in product(nodes, nodes):
        dist[u][v] = weight_func(u, v)

    iteration_callback(dist)

    for _ in range(len(nodes) - 1):
        tmp = deepcopy(dist)
        for u, v in product(nodes, nodes):
            if u == v:
                continue

            for mid in nodes:
                if mid == u or mid == v:
                    continue

                if dist[u][v] > dist[u][mid] + dist[mid][v]:
                    tmp[u][v] = dist[u][mid] + dist[mid][v]
                    prev[u][v] = mid

        dist = tmp
        iteration_callback(dist)

    iteration_callback(prev)


__all__ = [
    "bellman_ford"
]
