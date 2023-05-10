import threading
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
    q_output_sem = threading.Semaphore(0)
    q_input_sem = threading.Semaphore(1)
    q = AtomicQueue()
    threads_status = [False for _ in range(len(generators))]

    @threadify
    def yield_from_one(thread_id: int, gen):
        nonlocal threads_status
        # try:
        for v in gen:
            q.push(v)
        threads_status[thread_id] = True
        #     while True:
        #         q_input_sem.acquire()
        #         q.push(next(gen))
        #         q_input_sem.release()
        #         q_output_sem.release()
        # except StopIteration:
        #     threads_status[thread_id] = True

    for i, gen in enumerate(generators):
        yield_from_one(i, gen)

    # busy waiting
    while not all(threads_status):
        # q_output_sem.acquire()
        while not q.is_empty():
            yield q.pop()
    if not q.is_empty():
        yield from q


__all__ = [
    "join_generators"
]
