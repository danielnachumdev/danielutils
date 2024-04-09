import inspect
import functools
import multiprocessing

from ..reflection import get_prev_frame
from ..multi_x import process_id
import pickle


def processify(func):
    """Modifies the function so that when calling it, a new process
    will start to run it with provided arguments. Note that no return
    value will be given.

    Args:
        func (Callable): the function to make a process

    Returns:
        Callable: the modified function
    """
    multiprocessing.freeze_support()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        main_pid = kwargs.get("__main_pid", process_id())
        if process_id() == main_pid:
            frame = get_prev_frame(2)
            dct = {k: v for k, v in frame.f_globals.items() if type(v) != type(inspect)}
            p = multiprocessing.Process(target=_run_func, args=(main_pid, dct, func.__name__, args, kwargs))
            p.start()
            p.join()  # Optionally wait for the process to finish
        else:
            del kwargs["__main_pid"]
            return func(*args, **kwargs)

    return wrapper



def _run_func(main_pid: int, dct: dict, func_name: str, args, kwargs) -> None:
    return dct[func_name](*args, __main_pid=main_pid, **kwargs)

def debug_info(include_builtins: bool = False) -> dict:
    f = get_prev_frame(2)
    g = {k: v for k, v in f.f_globals.items() if k != "__builtins__"} if not include_builtins else dict(f.f_globals)
    return {
        "file": f.f_code.co_filename,
        "function": f.f_code.co_qualname,
        "line": f.f_lineno,
        "globals": g,
        "locals": dict(f.f_locals)
    }


__all__ = [
    "processify"
]
