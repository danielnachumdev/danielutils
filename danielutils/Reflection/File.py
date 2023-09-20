import inspect
import os
from typing import Optional, cast
from types import FrameType
from .get_prev_frame import get_prev_frame


def get_filename() -> Optional[str]:
    """returns the name of the file that this functions is called from

    Returns:
        Optional[str]: name of file
    """
    frame = get_prev_frame(inspect.currentframe())
    if frame is None:
        return None
    frame = cast(FrameType, frame)
    return frame.f_code.co_filename


def get_caller_filename() -> Optional[str]:
    """return the name of the file that the caller of the 
    function that's using this function is in

    Returns:
        Optional[str]: name of file
    """
    frame = get_prev_frame(get_prev_frame(inspect.currentframe()))
    if frame is None:
        return None
    frame = cast(FrameType, frame)
    return frame.f_code.co_filename


def get_current_directory() -> str:
    return os.path.dirname(os.path.abspath(get_caller_filename()))  # type:ignore # noqa


__all__ = [
    "get_filename",
    "get_caller_filename",
    'get_current_directory',
]
