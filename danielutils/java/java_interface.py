import inspect
from abc import abstractmethod
from typing import Protocol, runtime_checkable, Any, Callable
from ..reflection import ClassInfo


@runtime_checkable
class JavaInterface(Protocol):
    @staticmethod
    def definition(func: Callable) -> Callable:
        return abstractmethod(func)

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        info = ClassInfo(cls)
        print(info)
        super().__init_subclass__(**kwargs)

    @classmethod
    def is_implemented_by(interface, cls) -> bool:
        pass

    @classmethod
    def implements(cls, interface) -> bool:
        pass


definition = JavaInterface.definition
__all__ = [
    "JavaInterface",
    "definition"
]
