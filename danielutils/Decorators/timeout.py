import threading
import functools
from typing import Callable
from .validate import validate


@validate
def timeout(duration: int | float, /, *, silent: bool = False) -> Callable:
    """A decorator to limit runtime for a function

    Args:
        duration (int | float): allowed runtime duration
        silent (bool, optional): keyword only argument whether to pass the exception up the call stack. Defaults to False.

    Raises:
        ValueError: if a function is not provided to be decorated
        Exception: any exception from within the function

    Returns:
        Callable: the result decorated function
    """
    # https://stackoverflow.com/a/21861599/6416556
    def timeout_deco(func: Callable) -> Callable:
        if not isinstance(func, Callable):
            raise ValueError("timeout must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [
                TimeoutError(f'{func.__module__}.{func.__qualname__} timed out after {duration} seconds!')]

            def timeout_wrapper() -> None:
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as function_error:
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
