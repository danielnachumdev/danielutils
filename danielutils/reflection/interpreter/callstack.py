import inspect
from typing import Optional
from types import FrameType


def _get_prev_frame_from(frame: Optional[FrameType]) -> Optional[FrameType]:
    """Get the previous frame (caller's frame) in the call stack."""
    return frame.f_back if frame is not None else None


def get_current_frame() -> Optional[FrameType]:
    return _get_prev_frame_from(inspect.currentframe())


def get_prev_frame(n_steps: int = 1) -> Optional[FrameType]:
    if (f := get_current_frame()) is None:
        return None
    i = 0
    while i < n_steps:
        if (f := f.f_back) is None:
            return None
        i += 1
    return f


def get_prev_line_of_code(n_steps: int = 1) -> Optional[str]:
    frame = get_prev_frame(n_steps + 1)
    if frame is None:
        return None
    file = frame.f_back.f_code.co_filename  # type:ignore
    line_number = frame.f_back.f_lineno - 1  # type:ignore
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    line = lines[line_number]
    return line


__all__ = [
    "get_current_frame",
    "get_prev_frame",
    "get_prev_line_of_code"
]
