
from abc import abstractmethod, ABC
from typing import Protocol, runtime_checkable, Any, Callable, ParamSpec, Generic
from ..reflection import ClassInfo


class InterfaceError(Exception):
    ...


# @runtime_checkable
class JavaInterface(ABC):
    InterfaceError = InterfaceError

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        info = ClassInfo(cls)
        for base in info.bases:
            if base.name == JavaInterface.__name__:
                setattr(cls, "__is_interface__", True)
                break
        else:
            setattr(cls, "__is_interface__", False)
            info = ClassInfo(cls)
            print(set(info.functions))
            print(set(info.inherited_methods))
            actual_func_names = set(f.name for f in info.functions)
            for to_remove in {"__class_getitem__", "__init_subclass__"}:
                if hasattr(cls, to_remove) and getattr(cls, to_remove, None) is getattr(JavaInterface, to_remove, None):
                    actual_func_names.remove(to_remove)
            for interface in (base for base in cls.__mro__ if getattr(base, "__is_interface__", False)):
                expected_func_names = set(f.name for f in ClassInfo(interface).abstract_methods)
                if subtraction := expected_func_names.difference(actual_func_names):
                    raise InterfaceError(
                        f"class '{cls.__name__}' does not implement required methods {subtraction}")
        super().__init_subclass__(**kwargs)


__all__ = [
    "JavaInterface",
]
