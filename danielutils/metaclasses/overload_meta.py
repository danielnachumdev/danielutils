import functools
from typing import Callable
from ..decorators import overload


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
        # og_getattribute = None
        # if "__getattribute__" in namespace:
        #     og_getattribute = namespace["__getattribute__"]

        # def __getattribute__(self, name: str) -> Any:
        #     if not hasattr(type(self), name):
        #         if og_getattribute:
        #             return og_getattribute(self, name)
        #         return object.__getattribute__(self, name)

        #     function_obj: OverloadMeta.overload = getattr(
        #         type(self), name)

        #     @functools.wraps(function_obj)
        #     def wrapper(*args, **kwargs):
        #         return function_obj(self, *args, **kwargs)

        #     return wrapper

        def create_wrapper(v: overload):
            @functools.wraps(next(iter(v._functions.values()))[0])  # type:ignore# pylint: disable=protected-access
            def wrapper(*args, **kwargs):
                return v(*args, **kwargs)

            return wrapper

        for k, v in namespace.items():
            if isinstance(v, overload):  # type:ignore
                namespace[k] = create_wrapper(v)
        # namespace["__getattribute__"] = __getattribute__

        return super().__new__(mcs, name, bases, namespace)


__all__ = [
    "OverloadMeta"
]
