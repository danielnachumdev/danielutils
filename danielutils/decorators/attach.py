import functools
import logging
from typing import Callable, Optional, TypeVar
from .validate import validate
from ..versioned_imports import ParamSpec
from danielutils.logging_.utils import get_logger
from .logging_.utils import get_logger
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
    logger.debug(f"Creating attach decorator with before={before}, after={after}")
    if before is None and after is None:
        logger.error("Both before and after functions are None")
        raise ValueError("You must supply at least one function")

    def attach_deco(func: FuncT) -> FuncT:
        logger.debug(f"Applying attach decorator to function {func.__name__}")
        if not callable(func):
            logger.error(f"Object {func} is not callable")
            raise ValueError("attach must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Executing attached function {func.__name__}")
            if before is not None:
                logger.debug(f"Calling before function: {before.__name__}")
                before()
            res = func(*args, **kwargs)
            if after is not None:
                logger.debug(f"Calling after function: {after.__name__}")
                after()
            logger.debug(f"Attached function {func.__name__} completed")
            return res

        logger.debug(f"Attach decorator applied to {func.__name__}")
        return wrapper

    return attach_deco


__all__ = [
    "attach"
]
