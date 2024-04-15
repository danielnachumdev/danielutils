import threading
import functools
from typing import Callable, TypeVar, Union
from .validate import validate
from ..reflection import get_python_version

if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # type:ignore # pylint: disable=ungrouped-imports
T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate
def timeout(duration: Union[int, float], silent: bool = False) -> Callable[[FuncT], FuncT]:
    """A decorator to limit runtime for a function

    Args:
        duration (Union[int, float]): allowed runtime duration
        silent (bool, optional): keyword only argument whether
        to pass the exception up the call stack. Defaults to False.

    Raises:
        ValueError: if a function is not provided to be decorated
        Exception: any exception from within the function

    Returns:
        Callable: the result decorated function
    """

    # https://stackoverflow.com/a/21861599/6416556
    def timeout_deco(func: FuncT) -> FuncT:
        if not callable(func):
            raise ValueError("timeout must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res: list = [
                TimeoutError(f'{func.__module__}.{func.__qualname__} timed out after {duration} seconds!')]

            def timeout_wrapper() -> None:
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as function_error:  # pylint : disable=broad-exception-caught
                    res[0] = function_error

            t = threading.Thread(target=timeout_wrapper, daemon=True)
            try:
                t.start()
                t.join(duration)
            except Exception as thread_error:
                raise thread_error
            if isinstance(res[0], BaseException):
                if not silent:
                    raise res[0]
                return None
            return res[0]

        return wrapper

    return timeout_deco


__all__ = [
    "timeout"
]
