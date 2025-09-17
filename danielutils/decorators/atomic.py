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
    logger.debug("Making function %s atomic (thread-safe)", func.__name__)
    lock = threading.Lock()

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug("Acquiring lock for atomic function %s", func.__name__)
        with lock:
            logger.debug("Executing atomic function %s", func.__name__)
            result = func(*args, **kwargs)
            logger.debug("Atomic function %s completed", func.__name__)
            return result

    logger.debug("Atomic decorator applied to %s", func.__name__)
    return wrapper


__all__ = [
    "atomic"
]
