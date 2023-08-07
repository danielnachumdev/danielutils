from typing import Generator, Any, Tuple as t_tuple
from threading import Semaphore  # , Condition
from ..Decorators import threadify
from ..DataStructures import AtomicQueue, Queue
from ..Classes import AtomicCounter
# from ..Print import aprint
from ..Reflection import get_python_version
if get_python_version() >= (3, 9):
    from builtins import tuple as t_tuple  # type:ignore


def join_generators_busy_waiting(*generators) -> Generator[t_tuple[int, Any], None, None]:
    """joins an arbitrary amount of generators to yield objects as soon someone yield an object

    Yields:
        Generator[tuple[int, Any], None, None]: resulting generator
    """
    q = AtomicQueue()
    threads_status = [False for _ in range(len(generators))]

    @threadify
    def yield_from_one(thread_id: int, generator: Generator):
        nonlocal threads_status
        for v in generator:
            q.push((thread_id, v))
        threads_status[thread_id] = True

    for i, gen in enumerate(generators):
        yield_from_one(i, gen)

    # busy waiting
    while not all(threads_status):
        while not q.is_empty():
            yield q.pop()
    if not q.is_empty():
        yield from q


def join_generators(*generators) -> Generator[t_tuple[int, Any], None, None]:
    """will join generators to yield from all of them simultaneously 
    without busy waiting, using semaphores and multithreading 

    Yields:
        Generator[Any, None, None]: one generator that combines all of the given ones
    """
    queue = Queue()
    edit_queue_semaphore = Semaphore(1)
    queue_status_semaphore = Semaphore(0)
    finished_threads_counter = AtomicCounter()

    @threadify
    def thread_entry_point(index: int, generator: Generator) -> None:
        for value in generator:
            with edit_queue_semaphore:
                queue.push((index, value))
            queue_status_semaphore.release()
        finished_threads_counter.increment()

        if finished_threads_counter.get() == len(generators):
            # re-release the lock once from the last thread because it
            # gets stuck in the main loop after the generation has stopped
            queue_status_semaphore.release()

    for i, generator in enumerate(generators):
        thread_entry_point(i, generator)

    while finished_threads_counter.get() < len(generators):
        queue_status_semaphore.acquire()
        with edit_queue_semaphore:
            # needed for the very last iteration of the "while" loop. see above comment
            if not queue.is_empty():
                yield queue.pop()
    with edit_queue_semaphore:
        for value in queue:
            yield value


__all__ = [
    "join_generators_busy_waiting",
    "join_generators"
]
