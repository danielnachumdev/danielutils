from typing import Callable
import time


def measure(func: Callable) -> Callable:
    """A function to measure the execution time of a function.

    Args:
        func (function): The function to be measured.

    Returns:
        float: The time taken in seconds to execute the given function.
    """
    def wrapper(*args, **kwargs) -> float:
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        return end-start
    return wrapper


__all__ = [
    "measure",
]
