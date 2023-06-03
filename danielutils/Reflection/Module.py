from typing import Any
import importlib


def dynamically_load(module_name: str, obj_name: str) -> Any:
    """dynamically loads the module and returns the object from this file

    Args:
        module_name (str): name of python module, (typically a file name without extension)
        obj_name (str): the name of the wanted object

    Returns:
        Any: the object
    """
    return getattr(importlib.import_module(module_name), obj_name)


__all__ = [
    "dynamically_load"
]
