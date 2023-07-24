import functools
from typing import Callable, Any, TypeVar
import threading
from .validate import validate

from ..Reflection import get_python_version
if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # type:ignore # pylint: disable=ungrouped-imports
T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate
def atomic(func: FuncT) -> FuncT:
    """will make function thread safe by making it
    accessible for only one thread at one time

    Args:
        func (Callable): function to make thread safe

    Returns:
        Callable: the thread safe function
    """
    lock = threading.Lock()

    @ functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        with lock:
            return func(*args, **kwargs)
    return wrapper


__all__ = [
    "atomic"
]
