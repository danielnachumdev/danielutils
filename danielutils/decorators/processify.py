import inspect
import functools
import multiprocessing
import logging
from typing import Any, Dict

from ..reflection import get_prev_frame
from ..abstractions.multiprogramming import process_id
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def processify(func):
    """Modifies the function so that when calling it, a new process
    will start to run it with provided arguments. Note that no return
    value will be given.

    Args:
        func (Callable): the function to make a process

    Returns:
        Callable: the modified function
    """
    logger.debug("Creating processify decorator for function %s", func.__name__)
    multiprocessing.freeze_support()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        main_pid = kwargs.get("__main_pid", process_id())
        current_pid = process_id()
        logger.debug("Processify wrapper called for %s, main_pid=%s, current_pid=%s", func.__name__, main_pid, current_pid)
        
        if current_pid == main_pid:
            logger.info("Starting new process for function %s", func.__name__)
            frame = get_prev_frame(2)  # type:ignore
            dct = {k: v for k, v in frame.f_globals.items() if type(v) != type(inspect)}   # type:ignore
            logger.debug("Process context prepared with %s global variables", len(dct))
            p = multiprocessing.Process(target=_run_func, args=(main_pid, dct, func.__name__, args, kwargs))
            p.start()
            logger.debug("Process started for %s, PID: %s", func.__name__, p.pid)
            p.join()  # Optionally wait for the process to finish
            logger.info("Process completed for %s", func.__name__)
        else:
            logger.debug("Executing %s in child process", func.__name__)
            del kwargs["__main_pid"]
            return func(*args, **kwargs)

    logger.debug("Processify decorator applied to %s", func.__name__)
    return wrapper


def _run_func(main_pid: int, dct: dict, func_name: str, args, kwargs) -> None:
    logger.debug("Running function %s in child process", func_name)
    return dct[func_name](*args, __main_pid=main_pid, **kwargs)


def debug_info(include_builtins: bool = False) -> Dict[str, Any]:
    f = get_prev_frame(2)
    if f is None:
        raise RuntimeError("Failed to get frame")
    g = {k: v for k, v in f.f_globals.items() if k != "__builtins__"} if not include_builtins else dict(f.f_globals)
    return {
        "file": f.f_code.co_filename,
        "function": f.f_code.co_qualname,  # type:ignore
        "line": f.f_lineno,
        "globals": g,
        "locals": dict(f.f_locals)
    }


__all__ = [
    "processify"
]
