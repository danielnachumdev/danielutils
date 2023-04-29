import functools
from typing import Callable
from .validate import validate


@validate(strict=False)
def attach(before: Callable = None, after: Callable = None) -> Callable:
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

    def attach_deco(func: Callable):
        if not isinstance(func, Callable):
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
