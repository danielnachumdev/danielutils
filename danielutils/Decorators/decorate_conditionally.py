import functools
from typing import Callable, Optional
from .validate import validate


@validate(strict=False)
def decorate_conditionally(decorator: Callable, predicate: bool | Callable[[], bool], args: Optional[list] = None, kwargs: Optional[dict] = None):
    """will decorate a function iff the predicate is True or returns True

    Args:
        decorator (Callable): the decorator to use
        predicate (bool | Callable[[], bool]): the predicate
    """

    def deco(func):
        @functools.wraps(func)
        def wrapper(*args2, **kwargs2):
            return func(*args2, **kwargs2)
        nonlocal args, kwargs
        if (predicate() if callable(predicate) else predicate):
            if args is None:
                args = []
            if kwargs is None:
                kwargs = dict()
            return decorator(*args, **kwargs)(func)
        return wrapper
    return deco


__all__ = [
    "decorate_conditionally"
]
