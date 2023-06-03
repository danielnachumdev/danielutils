import inspect
from typing import Optional, cast
from types import FrameType
from ._get_prev_frame import _get_prev_frame


def get_filename() -> Optional[str]:
    """returns the name of the file that this functions is called from

    Returns:
        Optional[str]: name of file
    """
    frame = _get_prev_frame(inspect.currentframe())
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
    frame = _get_prev_frame(_get_prev_frame(inspect.currentframe()))
    if frame is None:
        return None
    frame = cast(FrameType, frame)
    return frame.f_code.co_filename


__all__ = [
    "get_filename",
    "get_caller_filename"
]
