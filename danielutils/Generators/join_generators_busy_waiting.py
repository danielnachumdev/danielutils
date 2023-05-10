from typing import Generator, Any
from ..Decorators import threadify
from ..MetaClasses import AtomicClassMeta
from ..DataStructures import Queue


class AtomicQueue(Queue, metaclass=AtomicClassMeta):
    pass


def join_generators_busy_waiting(*generators) -> Generator[Any, None, None]:
    """joins an arbitrary amount of generators to yield objects as soon someone yield an object

    Yields:
        Generator[Any, None, None]: resulting generator
    """
    q = AtomicQueue()
    threads_status = [False for _ in range(len(generators))]

    @threadify
    def yield_from_one(thread_id: int, gen):
        nonlocal threads_status
        for v in gen:
            q.push(v)
        threads_status[thread_id] = True

    for i, gen in enumerate(generators):
        yield_from_one(i, gen)

    # busy waiting
    while not all(threads_status):
        while not q.is_empty():
            yield q.pop()
    if not q.is_empty():
        yield from q


__all__ = [
    "join_generators_busy_waiting"
]
