import threading
import functools
import logging
from typing import Callable, TypeVar, Union
from .validate import validate
from ..versioned_imports import ParamSpec
from .logging_.utils import get_logger

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
    logger.debug(f"Creating timeout decorator with duration={duration}s, silent={silent}")

    # https://stackoverflow.com/a/21861599/6416556
    def timeout_deco(func: FuncT) -> FuncT:
        logger.debug(f"Applying timeout decorator to function {func.__name__}")
        if not callable(func):
            logger.error(f"Object {func} is not callable")
            raise ValueError("timeout must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Executing function {func.__name__} with timeout {duration}s")
            res: list = [
                TimeoutError(f'{func.__module__}.{func.__qualname__} timed out after {duration} seconds!')]

            def timeout_wrapper() -> None:
                try:
                    logger.debug(f"Starting timeout thread for {func.__name__}")
                    res[0] = func(*args, **kwargs)
                    logger.debug(f"Function {func.__name__} completed successfully in timeout thread")
                except Exception as function_error:  # pylint : disable=broad-exception-caught
                    logger.warning(f"Function {func.__name__} raised exception in timeout thread: {type(function_error).__name__}: {function_error}")
                    res[0] = function_error

            t = threading.Thread(target=timeout_wrapper, daemon=True)
            try:
                logger.debug(f"Starting timeout thread for {func.__name__}")
                t.start()
                t.join(duration)
                logger.debug(f"Timeout thread for {func.__name__} completed or timed out")
            except Exception as thread_error:
                logger.error(f"Thread error for {func.__name__}: {type(thread_error).__name__}: {thread_error}")
                raise thread_error
            if isinstance(res[0], BaseException):
                if not silent:
                    logger.warning(f"Function {func.__name__} timed out or raised exception: {type(res[0]).__name__}")
                    raise res[0]
                logger.debug(f"Function {func.__name__} timed out but silent mode enabled")
                return None
            logger.debug(f"Function {func.__name__} completed successfully within timeout")
            return res[0]

        logger.debug(f"Timeout decorator applied to {func.__name__}")
        return wrapper

    return timeout_deco


__all__ = [
    "timeout"
]
