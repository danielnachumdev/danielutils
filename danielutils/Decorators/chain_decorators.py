import functools
from typing import Callable


def chain_decorators(*decorators, reverse_order: bool = False) -> Callable:
    """will chain the given decorators in the order they appear

    Args:
        reverse_order (bool, optional): whether to reverse the order of decoration. Defaults to False.

    Returns:
        Callable: resulting multi-decorated function
    """
    def decorators_deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        for deco in decorators[::1 if reverse_order else -1]:
            wrapper = deco(wrapper)
        return wrapper
    return decorators_deco


__all__ = [
    "chain_decorators"
]
