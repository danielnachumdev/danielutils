
import logging
from abc import abstractmethod, ABC
from typing import Protocol, runtime_checkable, Any, Callable, ParamSpec, Generic
from ..reflection import ClassInfo
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class InterfaceError(Exception):
    ...


# @runtime_checkable
class JavaInterface(ABC):
    InterfaceError = InterfaceError

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        logger.info("Initializing JavaInterface subclass: %s", cls.__name__)
        info = ClassInfo(cls)
        
        # Check if this is a direct interface definition
        is_interface = False
        for base in info.bases:
            if base.name == JavaInterface.__name__:
                setattr(cls, "__is_interface__", True)
                is_interface = True
                break
        
        if not is_interface:
            setattr(cls, "__is_interface__", False)
            logger.debug("Validating interface compliance for implementation class: %s", cls.__name__)
            info = ClassInfo(cls)
            
            actual_func_names = set(f.name for f in info.functions)
            for to_remove in {"__class_getitem__", "__init_subclass__"}:
                if hasattr(cls, to_remove) and getattr(cls, to_remove, None) is getattr(JavaInterface, to_remove, None):
                    actual_func_names.remove(to_remove)
            
            # Validate interface implementation
            for interface in (base for base in cls.__mro__ if getattr(base, "__is_interface__", False)):
                expected_func_names = set(f.name for f in ClassInfo(interface).abstract_methods)
                
                if subtraction := expected_func_names.difference(actual_func_names):
                    error_msg = f"class '{cls.__name__}' does not implement required methods {subtraction}"
                    logger.error("Interface validation failed: %s", error_msg)
                    raise InterfaceError(error_msg)
                else:
                    logger.debug("Class %s successfully implements interface %s", cls.__name__, interface.__name__)
        
        logger.info("JavaInterface subclass %s initialized successfully", cls.__name__)
        super().__init_subclass__(**kwargs)


__all__ = [
    "JavaInterface",
]
