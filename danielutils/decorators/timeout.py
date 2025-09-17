import threading
import functools
import logging
from typing import Callable, TypeVar, Union
from .validate import validate
from ..versioned_imports import ParamSpec
from ..logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate  # type:ignore
def timeout(duration: Union[int, float], silent: bool = False) -> Callable[[FuncT], FuncT]:
    """A decorator to limit runtime for a function

    Args:
        duration (Union[int, float]): allowed runtime duration
        silent (bool, optional): keyword only argument whether
        to pass the exception up the call stack. Defaults to False.

    Raises:
        ValueError: if a function is not provided to be decorated
        Exception: any exception from within the function

    Returns:
        Callable: the result decorated function
    """
    logger.debug("Creating timeout decorator with duration=%ss, silent=%s", duration, silent)

    # https://stackoverflow.com/a/21861599/6416556
    def timeout_deco(func: FuncT) -> FuncT:
        logger.debug("Applying timeout decorator to function %s", func.__name__)
        if not callable(func):
            logger.error("Object %s is not callable", func)
            raise ValueError("timeout must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Executing function %s with timeout %ss", func.__name__, duration)
            res: list = [
                TimeoutError(f'{func.__module__}.{func.__qualname__} timed out after {duration} seconds!')]

            def timeout_wrapper() -> None:
                try:
                    logger.debug("Starting timeout thread for %s", func.__name__)
                    res[0] = func(*args, **kwargs)
                    logger.debug("Function %s completed successfully in timeout thread", func.__name__)
                except Exception as function_error:  # pylint : disable=broad-exception-caught
                    logger.warning("Function %s raised exception in timeout thread: %s: %s", func.__name__, type(function_error).__name__, function_error)
                    res[0] = function_error

            t = threading.Thread(target=timeout_wrapper, daemon=True)
            try:
                logger.debug("Starting timeout thread for %s", func.__name__)
                t.start()
                t.join(duration)
                logger.debug("Timeout thread for %s completed or timed out", func.__name__)
            except Exception as thread_error:
                logger.error("Thread error for %s: %s: %s", func.__name__, type(thread_error).__name__, thread_error)
                raise thread_error
            if isinstance(res[0], BaseException):
                if not silent:
                    logger.warning("Function %s timed out or raised exception: %s", func.__name__, type(res[0]).__name__)
                    raise res[0]
                logger.debug("Function %s timed out but silent mode enabled", func.__name__)
                return None
            logger.debug("Function %s completed successfully within timeout", func.__name__)
            return res[0]

        logger.debug("Timeout decorator applied to %s", func.__name__)
        return wrapper

    return timeout_deco


__all__ = [
    "timeout"
]
