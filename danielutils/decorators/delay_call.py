from typing import Callable, TypeVar, Union
import time
import functools
from .decorate_conditionally import decorate_conditionally
from .threadify import threadify

from ..reflection import get_python_version
if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # type:ignore# pylint: disable=ungrouped-imports
T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


def delay_call(seconds: Union[float, int], blocking: bool = True) -> Callable[[FuncT], FuncT]:
    """will delay the call to a function by the given amount of seconds

    Args:
        seconds (float | int): the amount of time to wait
        blocking (bool, optional): whether to block the main thread
        when waiting or to wait in a different thread. Defaults to True.
    """
    def deco(func: FuncT) -> FuncT:
        @decorate_conditionally(threadify, not blocking)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            func(*args, **kwargs)
        return wrapper
    return deco


__all__ = [
    "delay_call"
]
