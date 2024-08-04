import inspect
from typing import Protocol, runtime_checkable


# from ..reflection import is_function_annotated_properly


@runtime_checkable
class JavaInterface(Protocol):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        # print(cls.__qualname__)
        for func in cls.__dict__.values():
            if not callable(func): continue
            # if not is_function_annotated_properly(func):
            #     raise ValueError("When using a JavaInterface subclass, all function must be fully annotated.")
            src = inspect.getsourcelines(func)
            # print(func.__qualname__, src)
        pass
        return super().__init_subclass__(**kwargs)


__all__ = [
    "JavaInterface",
]
