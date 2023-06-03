from typing import Callable
from ..Decorators import overload


class OverloadMeta(type):
    @staticmethod
    def overload(func: Callable) -> overload:
        return overload(func)

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
            @functools.wraps(next(iter(v._functions.values()))[0])
            def wrapper(*args, **kwargs):
                return v(*args, **kwargs)
            return wrapper

        for k, v in namespace.items():
            if isinstance(v, overload):
                namespace[k] = create_wrapper(v)
        # namespace["__getattribute__"] = __getattribute__

        return super().__new__(mcs, name, bases, namespace)