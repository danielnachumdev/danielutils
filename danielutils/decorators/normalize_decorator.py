import functools
from typing import Callable, Any


def normalize_decorator(decorator: Callable[..., Any]) -> Callable[..., Any]:
    """

    Args:
        decorator: a function that is used as a decorator and you want to be used with "normalized" arguments

    Returns:
        object: 
        The normalized version of the decorator

    Example:

        Do
        ```python
        @normalize_decorator
        def validate(func, strict:bool = False):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # do stuff
                return func(*args, **kwargs)
            return wrapper
        ```

        instead of
        ```python
        def validate(strict_or_func: Optional[Union[bool,Callable]] = None):
            strict = False # default value
            def deco(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    # do stuff
                    return func(*args, **kwargs)
                return wrapper
            if isinstance(strict_or_func, bool):
                strict = strict_or_func
                return deco
            return deco(strict_or_func)
    """
    @functools.wraps(decorator)
    def wrapper(*args, **kwargs):
        if args and callable(args[0]):
            return decorator(args[0], *args[1:], **kwargs)
        else:
            return lambda func: decorator(func, *args, **kwargs)

    return wrapper


__all__ = [
    "normalize_decorator",
]
