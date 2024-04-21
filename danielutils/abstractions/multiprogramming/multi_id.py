import os
import threading


def process_id() -> int:
    """
    will return the current process' id
    Returns:
        int
    """
    return os.getpid()


def thread_id() -> int:
    """
    will return the current thread's id
    Returns:
        int
    """
    return threading.get_ident()


__all__ = [
    "process_id",
    "thread_id"
]
