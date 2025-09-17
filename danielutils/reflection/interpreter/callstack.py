import logging
import inspect
from typing import Optional
from types import FrameType
from ...logging_.utils import get_logger

logger = get_logger(__name__)


def _get_prev_frame_from(frame: Optional[FrameType]) -> Optional[FrameType]:
    """Get the previous frame (caller's frame) in the call stack."""
    return frame.f_back if frame is not None else None


def get_current_frame() -> Optional[FrameType]:
    logger.debug("Getting current frame")
    frame = _get_prev_frame_from(inspect.currentframe())
    logger.debug("Current frame: %s", frame)
    return frame


def get_prev_frame(n_steps: int = 1) -> Optional[FrameType]:
    logger.debug("Getting previous frame with %s steps", n_steps)
    if (f := get_current_frame()) is None:
        logger.debug("No current frame available")
        return None
    i = 0
    while i < n_steps:
        if (f := f.f_back) is None:
            logger.debug("Reached end of call stack at step %s", i)
            return None
        i += 1
    logger.debug("Found previous frame after %s steps", n_steps)
    return f


def get_prev_line_of_code(n_steps: int = 1) -> Optional[str]:
    logger.debug("Getting previous line of code with %s steps", n_steps)
    frame = get_prev_frame(n_steps + 1)
    if frame is None:
        logger.debug("No frame found for line of code")
        return None
    file = frame.f_back.f_code.co_filename  # type:ignore
    line_number = frame.f_back.f_lineno - 1  # type:ignore
    logger.debug("Reading line %s from file: %s", line_number, file)
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    line = lines[line_number]
    logger.debug("Previous line of code: %s", line.strip())
    return line


__all__ = [
    "get_current_frame",
    "get_prev_frame",
    "get_prev_line_of_code"
]
