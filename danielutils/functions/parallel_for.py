import logging
import threading
from typing import TypeVar, Callable
from .logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
Consumer = Callable[[T], None]


def parallel_for(func: Consumer[T], *args: T, wait: bool = True) -> None:
    """
    This function will run 'func' in parallel with the given args individually
    Args:
        func: function to run in parallel
        *args: args to call the function each time
        wait: whether to wait for all the threads to join before returning

    Returns:

    """
    logger.info(f"Starting parallel execution of {func.__name__} with {len(args)} arguments, wait={wait}")
    # this is safer... What if some other threads that were running will also end in the meantime?
    threads = [threading.Thread(target=func, args=[arg]) for arg in args]
    
    for t in threads:
        t.start()
    
    if wait:
        for t in threads:
            t.join()
        logger.info("All threads completed successfully")
    else:
        logger.info("Threads started, not waiting for completion")
    # before = threading.active_count()
    # for arg in args:
    #     threadify(func)(arg)
    #
    # if wait:
    #     while threading.active_count() > before:
    #         pass


__all__ = [
    'parallel_for'
]
