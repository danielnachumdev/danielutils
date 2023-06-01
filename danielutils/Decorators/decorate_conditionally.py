import functools
from typing import Callable, Optional
from .validate import validate


@validate(strict=False)
def decorate_conditionally(decorator: Callable, predicate: bool | Callable[[], bool], args: Optional[list] = None):
    """will decorate a function iff the predicate is True or returns True

    Args:
        decorator (Callable): the decorator to use
        predicate (bool | Callable[[], bool]): the predicate
    """

    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if (predicate() if callable(predicate) else predicate):
            if args is None:
                return decorator(func)
            return decorator(*args)(func)
        return wrapper
    return deco


__all__ = [
    "decorate_conditionally"
]
