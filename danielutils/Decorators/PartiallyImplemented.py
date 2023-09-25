from typing import Callable, Any, TypeVar
import functools
import platform
from .validate import validate
from ..colors import warning

from ..reflection import get_python_version
if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # type:ignore # pylint: disable=ungrouped-imports
T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


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
