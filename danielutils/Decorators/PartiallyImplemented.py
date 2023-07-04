from typing import Callable, Any, TypeVar, ParamSpec
import functools
from .validate import validate
from ..Colors import warning

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]


@validate
def PartiallyImplemented(func: FuncT) -> FuncT:
    """decorator to mark function as not fully implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """

    @ functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        warning(
            f"As marked by the developer, {func.__module__}.{func.__qualname__} "
            "may not be fully implemented and might not work properly.")
        return func(*args, **kwargs)
    return wrapper


__all__ = [
    "PartiallyImplemented"
]
