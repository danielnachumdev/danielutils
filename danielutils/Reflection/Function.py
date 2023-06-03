import inspect
from typing import cast, Optional, Callable
from types import FrameType
from ._get_prev_frame import _get_prev_frame


def get_caller_name(steps_back: int = 0) -> Optional[str]:
    """returns the name caller of the function

    Returns:
        str: name of caller

    USING THIS FUNCTION WHILE DEBUGGING WILL ADD ADDITIONAL FRAMES TO THE TRACEBACK
    """
    if not isinstance(steps_back, int):
        raise TypeError("steps_back must be an int")
    if not (steps_back >= 0):
        raise ValueError("steps_back must be a non-negative integer")
    # different implementation:

    # RGX = r'File ".*", line \d+, in (.+)\n'
    # # traceback_list = get_traceback()
    # # callee_frame = traceback_list[-1]
    # # callee_name = re.search(RGX, callee_frame).group(1)
    # # caller_frame = traceback_list[-2]
    # # caller_name = re.search(RGX, caller_frame).group(1)

    # this is more readable:

    # current_frame = inspect.currentframe()
    # callee_frame = current_frame.f_back
    # # callee_name = callee_frame.f_code.co_name
    # caller_frame = callee_frame.f_back
    # caller_name = caller_frame.f_code.co_name
    # return caller_name
    frame = _get_prev_frame(_get_prev_frame(inspect.currentframe()))
    if frame is None:
        return None
    frame = cast(FrameType, frame)
    while steps_back > 0:
        frame = _get_prev_frame(frame)
        if frame is None:
            return None
        frame = cast(FrameType, frame)
        steps_back -= 1
    return frame.f_code.co_name


def get_function_return_type(func: Callable, signature: Optional[inspect.Signature] = None) -> Optional[type]:
    """returns the return type of a function

    Args:
        func (Callable): a function to inquire about

    Returns:
        Optional[type]: the return type of the function
    """
    if signature is None:
        signature = inspect.signature(func)
    if ("inspect._empty" in str(signature.return_annotation)) or (signature.return_annotation is None):
        return type(None)
    return signature.return_annotation


__all__ = [
    "get_caller_name",
    "get_function_return_type"
]
