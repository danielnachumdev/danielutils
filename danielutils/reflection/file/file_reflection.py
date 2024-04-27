import inspect
import os
from typing import Optional, cast
from types import FrameType
from ..interpreter.callstack import _get_prev_frame_from


def get_caller_file_name() -> Optional[str]:
    """return the name of the file that the caller of the
    function that's using this function is in

    Returns:
        Optional[str]: name of file
    """
    frame = _get_prev_frame_from(_get_prev_frame_from(inspect.currentframe()))
    if frame is None:
        return None
    frame = cast(FrameType, frame)
    return frame.f_code.co_filename


def get_current_file_path() -> Optional[str]:
    """returns the name of the file that this functions is called from

    Returns:
        Optional[str]: name of file
    """
    return get_caller_file_name()


def get_current_file_name() -> Optional[str]:
    if (filepath := get_caller_file_name()) is None: return None
    return filepath.split('\\')[-1]


def get_current_folder_path() -> Optional[str]:
    if (filepath := get_caller_file_name()) is None: return None
    return "\\".join(filepath.split("\\")[:-1])


def get_current_folder_name() -> Optional[str]:
    if (filepath := get_caller_file_name()) is None: return None
    return filepath.split("\\")[-2]


def get_current_directory() -> str:
    """returns the name of the directory of main script"""
    return os.path.dirname(os.path.abspath(get_caller_file_name()))  # type:ignore # noqa


__all__ = [
    "get_current_file_path",
    "get_current_file_name",
    "get_current_folder_path",
    "get_current_folder_name",
    "get_caller_file_name",
    'get_current_directory',
]
