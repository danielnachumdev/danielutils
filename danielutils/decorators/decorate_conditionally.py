import functools
from typing import Callable, Optional, Union
from .validate import validate


@validate  # type:ignore(strict=False)
def decorate_conditionally(decorator: Callable, predicate: Union[bool, Callable[[], bool]], *,
                           decorator_args: Optional[list] = None, decorator_kwargs: Optional[dict] = None):
    """will decorate a function iff the predicate is True or returns True

    Args:
        decorator (Callable): the decorator to use
        predicate (bool | Callable[[], bool]): the predicate
    """

    def deco(func):
        if (predicate() if callable(predicate) else predicate):
            nonlocal decorator_args, decorator_kwargs, decorator
            if decorator_args is None:
                decorator_args = []
            if decorator_kwargs is None:
                decorator_kwargs = {}
            decorator = functools.wraps(func)(decorator)
            return decorator(*decorator_args, **decorator_kwargs)(func)
        return func

    return deco


__all__ = [
    "decorate_conditionally"
]
