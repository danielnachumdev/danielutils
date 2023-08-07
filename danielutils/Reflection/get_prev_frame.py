from typing import cast, Optional
from types import FrameType


def get_prev_frame(frame: Optional[FrameType]) -> Optional[FrameType]:
    """Get the previous frame (caller's frame) in the call stack.

    This function retrieves the frame that called the current frame in the Python call stack.

    Args:
        frame (Optional[FrameType]): The current frame for which to find the previous frame.

    Returns:
        Optional[FrameType]: The previous frame in the call stack, or None if it is not available.

    Note:
        If the input frame is None or not of type FrameType, the function returns None.
    """
    if frame is None:
        return None
    if not isinstance(frame, FrameType):
        return None
    frame = cast(FrameType, frame)
    return frame.f_back


__all__ = [
    "get_prev_frame"
]
