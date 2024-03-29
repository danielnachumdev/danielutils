import inspect
from .interpreter import get_python_version
if get_python_version() >= (3, 9):
    from builtins import list as t_list  # type:ignore
else:
    from typing import List as t_list


def get_explicitly_declared_functions(cls: type) -> t_list[str]:
    """
    Returns the names of the functions that are explicitly declared in a class.

    This function does not return inherited functions.

    Args:
        cls (type): The class to inspect.

    Returns:
        list[str]: A list of names of the functions explicitly declared in the class.
    """
    return [func for func, val in inspect.getmembers(cls, predicate=inspect.isfunction)]


__all__ = [
    "get_explicitly_declared_functions"
]
