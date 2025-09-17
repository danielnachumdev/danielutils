import logging
from typing import Optional
from .logging_.utils import get_logger

logger = get_logger(__name__)


class DeletedException(AttributeError):
    """an exception to be raised if a function is deleted
    """


def deleted(func, cls_name: Optional[str] = None):
    """replaces a function with a pre-scripted deleted function

    Args:
        func (_type_): _description_
        cls_name (Optional[str], optional): _description_. Defaults to None.

    Raises:
        DeletedException: _description_

    Returns:
        _type_: _description_
    """
    msg = f"'{func.__qualname__}' has been marked as deleted"
    if cls_name:
        msg = f"'{cls_name}.{func.__name__}' has been marked as deleted"

    def new_func(*args, **kwargs):  # pylint: disable=unused-argument
        nonlocal func
        logger.warning(f"Attempted to call deleted function: {func.__qualname__}")
        raise DeletedException(msg)
    return new_func


class ImplicitDataDeleterMeta(type):
    """Inheriting from this metaclass will 'delete' all non builtin function 
    and will replace them with a new function which will raise and error
    """
    def __new__(mcs, name, bases, namespace):
        logger.info(f"Creating ImplicitDataDeleterMeta class: {name}")
        
        cls_functions = set()
        for k, v in namespace.items():
            if callable(v):
                if hasattr(v, "__objclass__"):
                    if v.__objclass__ in {object}:
                        continue

                elif hasattr(v, "__module__"):
                    if v.__module__ in {'builtins', None}:
                        continue

                cls_functions.add(v)

        parent_functions = set()
        for base in bases:
            for k, v in base.__dict__.items():
                if callable(v):
                    parent_functions.add(v)

        parent_dct = {func.__name__: func for func in parent_functions}
        cls_dct = {func.__name__: func for func in cls_functions}
        to_delete = set({k: v for k, v in parent_dct.items()
                         if k not in cls_dct}.values())
        
        deleted_count = 0
        for func in to_delete:
            if func.__name__ in dir(object):
                if func.__name__ in {"__init__"}:
                    continue
                namespace[func.__name__] = object.__dict__[func.__name__]
            elif func.__name__ in {"__len__", "__bool__"}:
                namespace[func.__name__] = lambda self: True
            else:
                namespace[func.__name__] = deleted(func, name)
                deleted_count += 1

        logger.info(f"ImplicitDataDeleterMeta: {name} created with {deleted_count} functions marked as deleted")
        return super().__new__(mcs, name, bases, namespace)


__all__ = [
    "ImplicitDataDeleterMeta",
    "DeletedException"
]
