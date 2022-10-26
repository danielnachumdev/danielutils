from __future__ import annotations
from ..Decorators import validate
from ..Typing import Any, Tuple, Iterable, Union
from ..Functions import isoftype


class Node:
    def __init__(self, data: Any, next=None) -> None:
        self.data = data
        self.next = next

    def __str__(self) -> str:
        return f"Node(data={self.data}, next={self.next})"

    def __repr__(self) -> str:
        return str(self)


class Tree:
    pass


class BinaryTree(Tree):
    pass


class Stack:
    def __init__(self):
        self.data = []

    def pop(self) -> Any:
        if not self.is_empty():
            res = self.data[-1]
            self.data = self.data[:-1]
            return res

    def push(self, v: Any) -> None:
        self.data.append(v)

    def is_empty(self) -> bool:
        return len(self) == 0

    def __str__(self) -> str:
        s = ", ".join(str(v) for v in self.data)
        return f"Stack({s})"

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        return len(self.data)

    def top(self) -> Any:
        return self.data[-1]


class Queue:
    def __init__(self):
        self.data = []

    def dequeue(self) -> Any:
        if not self.is_empty():
            res = self.data[0]
            self.data = self.data[1:]
            return res

    def enqueue(self, v: Any) -> None:
        self.data.append(v)

    def is_empty(self) -> bool:
        return len(self) == 0

    def __str__(self) -> str:
        s = ", ".join(str(v) for v in self.data)
        return f"Stack({s})"

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        return len(self.data)


class LinkedList:
    pass
