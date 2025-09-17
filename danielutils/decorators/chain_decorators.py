import functools
import logging
from typing import Callable
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def chain_decorators(*decorators, reverse_order: bool = False) -> Callable:
    """will chain the given decorators in the order they appear

    Args:
        reverse_order (bool, optional): whether to reverse the order of decoration. Defaults to False.

    Returns:
        Callable: resulting multi-decorated function
    """
    logger.debug("Creating chain decorator with %s decorators, reverse_order=%s", len(decorators), reverse_order)
    def decorators_deco(func):
        logger.debug("Applying chain decorators to function %s", func.__name__)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Executing chained function %s", func.__name__)
            return func(*args, **kwargs)
        
        decorator_order = decorators[::1 if reverse_order else -1]
        logger.debug("Applying decorators in order: %s", [d.__name__ if hasattr(d, '__name__') else str(d) for d in decorator_order])
        for i, deco in enumerate(decorator_order):
            logger.debug("Applying decorator %s/%s: %s", i+1, len(decorator_order), deco.__name__ if hasattr(deco, '__name__') else str(deco))
            wrapper = deco(wrapper)
        
        logger.debug("Chain decorators applied to %s", func.__name__)
        return wrapper
    return decorators_deco


__all__ = [
    "chain_decorators"
]
