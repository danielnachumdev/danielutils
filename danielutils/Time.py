import time


def measure(func, *args, **kwargs) -> float:
    """A function to measure the execution time of a function.

    Args:
        func (function): The function to be measured.

    Returns:
        float: The time taken in seconds to execute the given function.
    """
    start = time.time()
    func(*args, **kwargs)
    end = time.time()
    return end-start


__all__ = [
    "measure",
]
