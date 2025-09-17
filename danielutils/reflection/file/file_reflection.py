import inspect
import logging
import os
from typing import Optional, cast
from types import FrameType
from ..interpreter.callstack import _get_prev_frame_from
from ...logging_.utils import get_logger

logger = get_logger(__name__)


def get_caller_file_name() -> Optional[str]:
    """return the name of the file that the caller of the
    function that's using this function is in

    Returns:
        Optional[str]: name of file
    """
    logger.debug("Getting caller file name")
    frame = _get_prev_frame_from(_get_prev_frame_from(inspect.currentframe()))
    if frame is None:
        logger.debug("No caller frame found")
        return None
    frame = cast(FrameType, frame)
    filename = frame.f_code.co_filename
    logger.debug("Caller file name: %s", filename)
    return filename


def get_current_file_path() -> Optional[str]:
    """returns the name of the file that this functions is called from

    Returns:
        Optional[str]: name of file
    """
    logger.debug("Getting current file path")
    return get_caller_file_name()


def get_current_file_name() -> Optional[str]:
    logger.debug("Getting current file name")
    if (filepath := get_caller_file_name()) is None: 
        logger.debug("No file path available")
        return None
    filename = filepath.split('\\')[-1]
    logger.debug("Current file name: %s", filename)
    return filename


def get_current_folder_path() -> Optional[str]:
    logger.debug("Getting current folder path")
    if (filepath := get_caller_file_name()) is None: 
        logger.debug("No file path available")
        return None
    folder_path = "\\".join(filepath.split("\\")[:-1])
    logger.debug("Current folder path: %s", folder_path)
    return folder_path


def get_current_folder_name() -> Optional[str]:
    logger.debug("Getting current folder name")
    if (filepath := get_caller_file_name()) is None: 
        logger.debug("No file path available")
        return None
    folder_name = filepath.split("\\")[-2]
    logger.debug("Current folder name: %s", folder_name)
    return folder_name


def get_current_directory() -> str:
    """returns the name of the directory of main script"""
    logger.debug("Getting current directory")
    directory = os.path.dirname(os.path.abspath(get_caller_file_name()))  # type:ignore # noqa
    logger.debug("Current directory: %s", directory)
    return directory


__all__ = [
    "get_current_file_path",
    "get_current_file_name",
    "get_current_folder_path",
    "get_current_folder_name",
    "get_caller_file_name",
    'get_current_directory',
]
