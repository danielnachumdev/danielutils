from typing import Callable, Optional
from types import FrameType
import signal


def register_signal_handler(signal_number: int, handler: Callable[[int, Optional[FrameType]], None]):
    """register a signal handler for specified signal

    Args:
        signal_number (int): signal number to handle
        handler (Callable[[int, FrameType], None]): the handler function
    """
    signal.signal(signal_number, handler)


__all__ = [
    "register_signal_handler"
]
