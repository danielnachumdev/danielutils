from typing import TypeVar
from ...metaclasses import AtomicClassMeta
from .queue import Queue

T = TypeVar("T")


class AtomicQueue(Queue[T], metaclass=AtomicClassMeta):
    """Same as Queue but atomic
    """


__all__ = [
    "AtomicQueue"
]
