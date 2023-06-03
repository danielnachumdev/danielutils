from typing import cast, Optional
from types import FrameType


def _get_prev_frame(frame: Optional[FrameType]) -> Optional[FrameType]:
    if frame is None:
        return None
    if not isinstance(frame, FrameType):
        return None
    frame = cast(FrameType, frame)
    return frame.f_back


__all__ = [
    "_get_prev_frame"
]
