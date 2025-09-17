import functools
import logging
from typing import Callable, Any, TypeVar
import threading
from .validate import validate
from ..logging_.utils import get_logger
logger = get_logger(__name__)

from ..versioned_imports import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate  # type:ignore
def atomic(func: FuncT) -> FuncT:
    """will make function thread safe by making it
    accessible for only one thread at one time

    Args:
        func (Callable): function to make thread safe

    Returns:
        Callable: the thread safe function
    """
    logger.debug(f"Making function {func.__name__} atomic (thread-safe)")
    lock = threading.Lock()

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(f"Acquiring lock for atomic function {func.__name__}")
        with lock:
            logger.debug(f"Executing atomic function {func.__name__}")
            result = func(*args, **kwargs)
            logger.debug(f"Atomic function {func.__name__} completed")
            return result

    logger.debug(f"Atomic decorator applied to {func.__name__}")
    return wrapper


__all__ = [
    "atomic"
]
