from typing import Generator, Any
from ..Decorators import threadify
from ..MetaClasses import AtomicClassMeta
from ..DataStructures import Queue


class AtomicQueue(Queue, metaclass=AtomicClassMeta):
    pass


def join_generators(*generators) -> Generator[Any, None, None]:
    """joins an arbitrary amount of generators to yield objects as soon someone yield an object

    Yields:
        Generator[Any, None, None]: resulting generator
    """
    q = AtomicQueue()
    statuses = [False for _ in range(len(generators))]

    @threadify
    def yield_from_one(thread_id: int, gen):
        nonlocal statuses
        try:
            while True:
                q.push(next(gen))
        except StopIteration:
            statuses[thread_id] = True

    for i, gen in enumerate(generators):
        yield_from_one(i, gen)

    while not all(statuses):
        while q.is_empty():
            pass
        yield q.pop()


__all__ = [
    "join_generators"
]
