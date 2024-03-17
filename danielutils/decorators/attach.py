import functools
from typing import Callable, Optional, TypeVar
import platform
from .validate import validate
from ..reflection import get_python_version
if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # type:ignore # pylint: disable=ungrouped-imports
T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate(strict=False)
def attach(before: Optional[Callable] = None, after: Optional[Callable] = None) -> Callable[[FuncT], FuncT]:
    """attaching functions to a function

    Args:
        before (Callable, optional): function to call before. Defaults to None.
        after (Callable, optional): function to call after. Defaults to None.

    Raises:
        ValueError: if both before and after are none
        ValueError: if the decorated object is not a Callable

    Returns:
        Callable: the decorated result
    """
    if before is None and after is None:
        raise ValueError("You must supply at least one function")

    def attach_deco(func: FuncT) -> FuncT:
        if not callable(func):
            raise ValueError("attach must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if before is not None:
                before()
            res = func(*args, **kwargs)
            if after is not None:
                after()
            return res
        return wrapper
    return attach_deco


__all__ = [
    "attach"
]
