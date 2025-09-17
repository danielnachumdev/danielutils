import functools
import logging
from typing import Callable, Optional, TypeVar
from .validate import validate
from ..versioned_imports import ParamSpec
from ..logging_.utils import get_logger
logger = get_logger(__name__)

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate(strict=False)  # type:ignore
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
    logger.debug("Creating attach decorator with before=%s, after=%s", before, after)
    if before is None and after is None:
        logger.error("Both before and after functions are None")
        raise ValueError("You must supply at least one function")

    def attach_deco(func: FuncT) -> FuncT:
        logger.debug("Applying attach decorator to function %s", func.__name__)
        if not callable(func):
            logger.error("Object %s is not callable", func)
            raise ValueError("attach must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Executing attached function %s", func.__name__)
            if before is not None:
                logger.debug("Calling before function: %s", before.__name__)
                before()
            res = func(*args, **kwargs)
            if after is not None:
                logger.debug("Calling after function: %s", after.__name__)
                after()
            logger.debug("Attached function %s completed", func.__name__)
            return res

        logger.debug("Attach decorator applied to %s", func.__name__)
        return wrapper

    return attach_deco


__all__ = [
    "attach"
]
