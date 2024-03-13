import os
import threading


def process_id() -> int:
    return os.getpid()


def thread_id() -> int:
    return threading.get_ident()


__all__ = [
    "process_id",
    "thread_id"
]
