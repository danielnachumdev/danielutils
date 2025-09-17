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
    logger.debug(f"Creating processify decorator for function {func.__name__}")
    multiprocessing.freeze_support()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        main_pid = kwargs.get("__main_pid", process_id())
        current_pid = process_id()
        logger.debug(f"Processify wrapper called for {func.__name__}, main_pid={main_pid}, current_pid={current_pid}")
        
        if current_pid == main_pid:
            logger.info(f"Starting new process for function {func.__name__}")
            frame = get_prev_frame(2)  # type:ignore
            dct = {k: v for k, v in frame.f_globals.items() if type(v) != type(inspect)}   # type:ignore
            logger.debug(f"Process context prepared with {len(dct)} global variables")
            p = multiprocessing.Process(target=_run_func, args=(main_pid, dct, func.__name__, args, kwargs))
            p.start()
            logger.debug(f"Process started for {func.__name__}, PID: {p.pid}")
            p.join()  # Optionally wait for the process to finish
            logger.info(f"Process completed for {func.__name__}")
        else:
            logger.debug(f"Executing {func.__name__} in child process")
            del kwargs["__main_pid"]
            return func(*args, **kwargs)

    logger.debug(f"Processify decorator applied to {func.__name__}")
    return wrapper


def _run_func(main_pid: int, dct: dict, func_name: str, args, kwargs) -> None:
    logger.debug(f"Running function {func_name} in child process")
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
