import inspect
from abc import abstractmethod
from typing import Protocol, runtime_checkable, Any, Callable


# from ..reflection import is_function_annotated_properly


@runtime_checkable
class JavaInterface(Protocol):
    @staticmethod
    def definition(func: Callable) -> Callable:
        return abstractmethod(func)

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        # print(cls.__qualname__)
        for func in cls.__dict__.values():
            if not callable(func): continue
            # if not is_function_annotated_properly(func):
            #     raise ValueError("When using a JavaInterface subclass, all function must be fully annotated.")
            src = inspect.getsourcelines(func)
            pass
            # print(func.__qualname__, src)
        pass
        super().__init_subclass__(**kwargs)


definition = JavaInterface.definition
__all__ = [
    "JavaInterface",
    "definition"
]
