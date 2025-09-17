import functools
import re
import traceback
import logging
from typing import Any, Callable, TypeVar
from .validate import validate
from ..colors import warning
from ..versioned_imports import ParamSpec
from ..logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate  # type:ignore
def limit_recursion(max_depth: int, return_value: Any = None, quiet: bool = True) -> Callable[[FuncT], FuncT]:
    """decorator to limit recursion of functions

    Args:
        max_depth (int): max recursion depth which is allowed for this function
        return_value (Any, optional): The value to return when the limit is reached. Defaults to None.
            if is None, will return the last a tuple for the last args, kwargs given
        quiet (bool, optional): whether to print a warning message. Defaults to True.
    """
    logger.debug(f"Creating limit_recursion decorator with max_depth={max_depth}, quiet={quiet}")

    def deco(func: FuncT) -> FuncT:
        logger.debug(f"Applying limit_recursion decorator to function {func.__name__}")
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            depth = functools.reduce(
                lambda count, line:
                count + 1 if re.search(rf"{func.__name__}\(.*\)$", line)
                else count,
                traceback.format_stack(), 0
            )
            logger.debug(f"Function {func.__name__} called at recursion depth {depth}/{max_depth}")
            if depth >= max_depth:
                logger.warning(f"Recursion limit reached for {func.__name__} at depth {depth}")
                if not quiet:
                    warning(
                        "limit_recursion has limited the number of calls for "
                        f"{func.__module__}.{func.__qualname__} to {max_depth}")
                if return_value:
                    logger.debug(f"Returning specified return_value: {return_value}")
                    return return_value
                logger.debug(f"Returning args and kwargs: {args}, {kwargs}")
                return args, kwargs
            logger.debug(f"Recursion depth {depth} is within limit, calling function")
            return func(*args, **kwargs)

        logger.debug(f"Limit_recursion decorator applied to {func.__name__}")
        return wrapper

    return deco


__all__ = [
    "limit_recursion"
]
