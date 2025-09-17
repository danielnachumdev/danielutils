import logging
from typing import Generator, Any, Tuple as Tuple
from threading import Semaphore  # , Condition
from ..decorators import threadify
from ..data_structures import AtomicQueue, Queue
from ..better_builtins import AtomicCounter
# from ..Print import aprint
from ..reflection import get_python_version
from .logging_.utils import get_logger

logger = get_logger(__name__)

if get_python_version() >= (3, 9):
    from builtins import tuple as Tuple  # type:ignore


def join_generators_busy_waiting(*generators) -> Generator[Tuple[int, Any], None, None]:
    """joins an arbitrary amount of generators to yield objects as soon someone yield an object

    Yields:
        Generator[tuple[int, Any], None, None]: resulting generator
    """
    logger.info(f"Starting join_generators_busy_waiting with {len(generators)} generators")
    q: AtomicQueue[Tuple[int, Any]] = AtomicQueue()
    threads_status = [False for _ in range(len(generators))]

    @threadify  # type:ignore
    def yield_from_one(thread_id: int, generator: Generator):
        nonlocal threads_status
        items_yielded = 0
        for v in generator:
            q.push((thread_id, v))
            items_yielded += 1
        logger.debug(f"Thread {thread_id} finished processing, yielded {items_yielded} items")
        threads_status[thread_id] = True

    for i, gen in enumerate(generators):
        yield_from_one(i, gen)

    # busy waiting
    total_yielded = 0
    while not all(threads_status):
        while not q.is_empty():
            item = q.pop()
            total_yielded += 1
            yield item
    if not q.is_empty():
        remaining_items = 0
        for item in q:
            remaining_items += 1
            yield item
    
    logger.info(f"join_generators_busy_waiting completed, yielded {total_yielded} items total")


def join_generators(*generators) -> Generator[Tuple[int, Any], None, None]:
    """will join generators to yield from all of them simultaneously 
    without busy waiting, using semaphores and multithreading 

    Yields:
        Generator[Any, None, None]: one generator that combines all of the given ones
    """
    logger.info(f"Starting join_generators with {len(generators)} generators")
    queue: Queue = Queue()
    edit_queue_semaphore = Semaphore(1)
    queue_status_semaphore = Semaphore(0)
    finished_threads_counter = AtomicCounter()

    @threadify  # type:ignore
    def thread_entry_point(index: int, generator: Generator) -> None:
        items_processed = 0
        for value in generator:
            with edit_queue_semaphore:
                queue.push((index, value))
            queue_status_semaphore.release()
            items_processed += 1
        logger.debug(f"Thread {index} finished processing, processed {items_processed} items")
        finished_threads_counter.increment()

        if finished_threads_counter.get() == len(generators):
            # re-release the lock once from the last thread because it
            # gets stuck in the main loop after the generation has stopped
            queue_status_semaphore.release()

    for i, generator in enumerate(generators):
        thread_entry_point(i, generator)

    total_yielded = 0
    while finished_threads_counter.get() < len(generators):
        queue_status_semaphore.acquire()
        with edit_queue_semaphore:
            # needed for the very last iteration of the "while" loop. see above comment
            if not queue.is_empty():
                item = queue.pop()
                total_yielded += 1
                yield item
    
    remaining_items = 0
    with edit_queue_semaphore:
        for value in queue:
            remaining_items += 1
            yield value
    
    logger.info(f"join_generators completed, yielded {total_yielded + remaining_items} items total")


__all__ = [
    "join_generators_busy_waiting",
    "join_generators"
]
