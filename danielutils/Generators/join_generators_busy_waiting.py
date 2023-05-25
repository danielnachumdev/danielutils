from typing import Generator, Any
from ..Decorators import threadify
from ..DataStructures import AtomicQueue, Queue
from ..Classes import AtomicCounter
from threading import Semaphore


def join_generators_busy_waiting(*generators) -> Generator[Any, Any, None]:
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


def join_generators(*generators) -> Generator[Any, None, None]:
    """will join generators to yield from all of them simultaneously without busy waiting, using semaphores and multithreading 

    Yields:
        Generator[Any, None, None]: one generator that combines all of the given ones
    """
    queue = Queue()
    edit_queue_semaphore = Semaphore(1)
    queue_status_semaphore = Semaphore(0)
    finished_threads_counter = AtomicCounter()

    @threadify
    def thread_entry_point(generator) -> None:
        for value in generator:
            with edit_queue_semaphore:
                queue.push(value)
            queue_status_semaphore.release()
        finished_threads_counter.increment()

    for generator in generators:
        thread_entry_point(generator)

    while finished_threads_counter.get() < len(generators):
        queue_status_semaphore.acquire()
        with edit_queue_semaphore:
            yield queue.pop()


__all__ = [
    "join_generators_busy_waiting",
    "join_generators"
]
