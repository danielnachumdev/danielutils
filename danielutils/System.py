from math import inf
from .Decorators import overload, timeout, validate
from .Typing import Tuple, IO
from .Exceptions import TimeoutError
from .Conversions import str_to_bytes
from pathlib import Path
import subprocess
import time


def cm(*args, shell: bool = True) -> Tuple[int, bytes, bytes]:
    """Execute windows shell command and return output

    Args:
        command or args:\n
        command (str): A string representation of the command to execute.
        args (list[str]): A list of all the command parts
        shell (bool, optional): whether to execute in shell. Defaults to True.

    Raises:
        TypeError: will raise if 'shell' is not boolean

    Returns:
        Tuple[int, bytes, bytes]: return code, stdout, stderr
    """
    if not isinstance(shell, bool):
        raise TypeError("In function 'cm' param 'shell' must be of type bool")
    if Path(args[0]).is_file():
        args = (f"\"{args[0]}\"", *args[1:])
    res = subprocess.run(*args, shell=shell, capture_output=True)
    return res.returncode, res.stdout, res.stderr


@validate([float, int])
def sleep(seconds: float):
    time.sleep(seconds)


def __acm_write(*args, p: subprocess.Popen, sep=" ", end="\n") -> None:
    b_args = str_to_bytes(sep).join(str_to_bytes(v) for v in args)
    b_end = str_to_bytes(end)
    p.stdin.write(b_args+b_end)
    p.stdin.flush()


def acm(command: str, inputs: list[str] = None, i_timeout: float = 0.01, cwd=None, env=None, shell: bool = False, use_write_helper: bool = True) -> tuple[int, list[bytes] | None, list[bytes] | None]:
    """Advanced command

    Args:
        command (str): The command to execute\n
        inputs (list[str]): the inputs to give to the program from the command. Defaults to None.\n
        i_timeout (float, optional): An individual timeout for every step of the execution. Defaults to 0.01.\n
        cwd (?, optional): Current working directory. Defaults to None.\n
        env (?, optional): Environment variables. Defaults to None.\n
        shell (bool, optional): whether to execute the command through shell. Defaults to False.\n
        use_write_helper (bool, optional): whether to parse each input as it would have been parse with builtin print() or to use raw text. Defaults to True.

    Raises:
        If @timeout will raise something other than TimeoutError.\n
        If the subprocess input and output handling will raise an exception.

    Returns:
        tuple[int, list[bytes] | None, list[bytes] | None]: return code, stdout, stderr
    """

    if inputs is None:
        inputs = []
    p = None
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, env=env, shell=shell)

        @timeout(i_timeout)
        def readlines(s: IO, l: list):
            l.extend(s.readlines())

        def extend_from_stream(stream: IO[bytes], list_to_extend_to: list):
            if stream is not None and stream.readable():
                try:
                    readlines(stream, list_to_extend_to)
                    # new_len = len(l)
                except TimeoutError:
                    # break
                    pass
                except BaseException as e1:
                    raise e1

        stdout: list[bytes] = []
        stderr: list[bytes] = []
        for input in inputs:
            if p.stdin.writable():
                if use_write_helper:
                    __acm_write(input, p=p)
                else:
                    __acm_write(input, p=p, sep="", end="")
            extend_from_stream(p.stdout, stdout)
            extend_from_stream(p.stderr, stderr)
        else:
            extend_from_stream(p.stdout, stdout)
            extend_from_stream(p.stderr, stderr)
        p.stdin.close()
        p.stdout.close()
        if p.stderr is not None:
            p.stderr.close()
        returncode = p.wait()
        return returncode, stdout, stderr
    except BaseException as e2:
        raise type(e2)(f"Maybe use shell=True? original error:\n{e2.args}")
    finally:
        if p is not None:
            if p.stdin is not None:
                p.stdin.close()
            if p.stderr is not None:
                p.stderr.close()
            if p.stdout is not None:
                p.stdout.close()


__all__ = [
    "cm",
    "acm",
    "sleep"
]
