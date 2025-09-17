import logging
from typing import Callable, TypeVar
import functools
import threading
from ..versioned_imports import ParamSpec
from ..logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


def threadify(func: FuncT) -> FuncT:
    """will modify the function that when calling it a new thread
    will start to run it with provided arguments.\nnote that no return value will be given

    Args:
        func (Callable): the function to make a thread

    Returns:
        Callable: the modified function
    """
    logger.debug("Creating threadify decorator for function %s", func.__name__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Starting thread for function %s", func.__name__)
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        logger.debug("Thread started for %s, thread_id=%s", func.__name__, thread.ident)

    logger.debug("Threadify decorator applied to %s", func.__name__)
    return wrapper


__all__ = [
    "threadify"
]
