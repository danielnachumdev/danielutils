import logging
import functools
from typing import Callable
from ..decorators import overload
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class OverloadMeta(type):
    """A meta-class for overloading functions in a class
    """

    @staticmethod  # type:ignore
    def overload(func: Callable) -> overload:
        """overloads a function

        Args:
            func (Callable): function ot overload

        Returns:
            overload: _description_
        """
        return overload(func)  # type:ignore

    def __new__(mcs, name, bases, namespace):
        logger.info(f"Creating overload class: {name}")
        
        def create_wrapper(v: overload):
            @functools.wraps(next(iter(v._functions.values()))[0])  # type:ignore# pylint: disable=protected-access
            def wrapper(*args, **kwargs):
                return v(*args, **kwargs)

            return wrapper

        overloaded_functions = 0
        for k, v in namespace.items():
            if isinstance(v, overload):  # type:ignore
                namespace[k] = create_wrapper(v)
                overloaded_functions += 1

        logger.info(f"OverloadMeta: {name} created with {overloaded_functions} overloaded functions")
        return super().__new__(mcs, name, bases, namespace)


__all__ = [
    "OverloadMeta"
]
