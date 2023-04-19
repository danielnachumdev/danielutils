from __future__ import annotations
from typing import Any


class Node:
    def __init__(self, data: Any = None, next: Node | list[Node] = None):
        self.data = data
        self.next = next

    def has_next(self) -> bool:
        return self.next is not None


__all__ = [
    "Node"
]
