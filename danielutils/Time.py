from typing import Callable, TypeVar
from typing_extensions import ParamSpec
import time
T = TypeVar("T")
P = ParamSpec("P")


def measure(func: Callable[P, T]) -> Callable[P, float]:
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
