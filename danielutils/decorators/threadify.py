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
    logger.debug(f"Creating threadify decorator for function {func.__name__}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Starting thread for function {func.__name__}")
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        logger.debug(f"Thread started for {func.__name__}, thread_id={thread.ident}")

    logger.debug(f"Threadify decorator applied to {func.__name__}")
    return wrapper


__all__ = [
    "threadify"
]
