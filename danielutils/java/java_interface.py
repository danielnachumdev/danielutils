import inspect
from abc import abstractmethod, ABC
from typing import Protocol, runtime_checkable, Any, Callable, ParamSpec, Generic
from ..reflection import ClassInfo

P = ParamSpec("P")


@runtime_checkable
class JavaInterface(Generic[P], Protocol[P]):
    @staticmethod
    def definition(func: Callable) -> Callable:
        return abstractmethod(func)

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        info = ClassInfo(cls)
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
