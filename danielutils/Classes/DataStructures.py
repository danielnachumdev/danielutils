from __future__ import annotations
from ..Decorators import validate
from typing import Any, Tuple, Iterable, Union
from ..Functions import isoftype


class tlist(list):
    def get_type_error_msg(self, v: Any):
        return f"Value is of wrong type:\n'{v}' of type '{type(v)}' buy should be of type '{self.type}'"
    """tlist is same as builtin python list but with added type restriction

    Args:
        type (type): the allowed type, can be nested type
        iterable (Iterable, optional): the value to create the tlist from. Defaults to None.
    """
    @validate(None, [type, Union], Iterable)
    def __init__(self, type: type, iterable: Iterable = None):
        """_summary_

        Args:
            type (type): the allowed type, can be nested type
        ietrable (Iterable, optional): the value to create the tlist from. Defaults to None.

        Raises:
            TypeError: _description_
        """
        self.type = type
        if iterable is not None:
            for v in iterable:
                if not isoftype(v, type):
                    raise TypeError(self.get_type_error_msg(v))
                super().append(v)

    def __setitem__(self, index: int, value: Any) -> None:
        if not isoftype(value, self.type):
            raise TypeError(self.get_type_error_msg(value))
        super()[index] = value

    def append(self, value: Any) -> None:
        if not isoftype(value, self.type):
            raise TypeError(self.get_type_error_msg(value))
        super().append(value)

    @validate(None, Iterable)
    def extend(self, iterable: Iterable) -> None:
        for v in iterable:
            self.append(v)

    def __add__(self, other) -> tlist:
        pass


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


class Graph:
    pass
