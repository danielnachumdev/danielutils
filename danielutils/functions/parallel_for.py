import threading
from typing import TypeVar, Callable

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
    # this is safer... What if some other threads that were running will also end in the meantime?
    threads = [threading.Thread(target=func, args=[arg]) for arg in args]
    for t in threads:
        t.start()
    if wait:
        for t in threads:
            t.join()
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
