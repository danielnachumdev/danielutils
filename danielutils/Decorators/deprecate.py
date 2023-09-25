import platform
from typing import Callable, TypeVar
from ..colors import warning, ColoredText

from ..reflection import get_python_version
if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # type:ignore # pylint: disable=ungrouped-imports
T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


def deprecate_with(replacement_func) -> Callable[[FuncT], FuncT]:
    """will replace a deprecated function with the replacement func and will print a warning"""
    def deco(func: FuncT) -> FuncT:
        warning(f"{func.__module__}.{func.__qualname__} is deprecated,"
                f" using {replacement_func.__module__}.{replacement_func.__qualname__} instead")

        def wrapper(*args, **kwargs):
            return replacement_func(*args, **kwargs)
        return wrapper
    return deco


def deprecate(deprecation_message: str) -> Callable[[FuncT], FuncT]:
    """A decorator to print a deprecation message when using a deprecated function

    Args:
        deprecation_message (str): deprecation message
    """
    def deco(func: FuncT) -> FuncT:
        def wrapper(*args, **kwargs):
            print(ColoredText.orange("Deprecation Warning") +
                  ":", deprecation_message)
            return func(*args, **kwargs)
        return wrapper
    return deco


__all__ = [
    "deprecate_with",
    "deprecate"
]
