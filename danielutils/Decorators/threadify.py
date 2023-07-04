from typing import Callable, ParamSpec
import functools
import threading

P = ParamSpec("P")
FuncT = Callable[P, None]


def threadify(func: FuncT) -> FuncT:
    """will modify the function that when calling it a new thread will start to run it with provided arguments.\nnote that no return value will be given

    Args:
        func (Callable): the function to make a thread

    Returns:
        Callable: the modified function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


__all__ = [
    "threadify"
]
