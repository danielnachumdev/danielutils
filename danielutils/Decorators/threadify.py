from typing import Callable
import platform
import functools
import threading

if platform.python_version() >= "3.9":
    from typing import ParamSpec
    P = ParamSpec("P")
    FuncT = Callable[P, None]
else:
    FuncT = Callable  # type:ignore


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
