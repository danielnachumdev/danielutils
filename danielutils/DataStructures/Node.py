from __future__ import annotations
from typing import Any


class Node:
    """classic Node implementation
    """

    def __init__(self, data: Any, nxt=None) -> None:
        self.data = data
        self.nxt = nxt

    def __str__(self) -> str:
        return f"Node(data={self.data}, next={self.nxt})"

    def __repr__(self) -> str:
        return str(self)


__all__ = [
    "Node"
]
