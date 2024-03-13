import inspect
from typing import Optional
from types import FrameType


def get_current_frame() -> Optional[FrameType]:
    return get_prev_frame_from(inspect.currentframe())


def get_prev_frame_from(frame: Optional[FrameType]) -> Optional[FrameType]:
    """Get the previous frame (caller's frame) in the call stack."""
    return frame.f_back if frame is not None else None


def get_n_prev_frame(n_steps: int = 1) -> Optional[FrameType]:
    if (f := get_current_frame()) is None:
        return None
    i = 0
    while i < n_steps:
        if (f := f.f_back) is None:
            return None
        i += 1
    return f


__all__ = [
    "get_current_frame",
    "get_prev_frame_from",
    "get_n_prev_frame"
]
