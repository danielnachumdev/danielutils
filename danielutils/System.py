from .Decorators import overload, timeout
from .Typing import Tuple, Union, IO
from .Conversions import str_to_bytes
import subprocess
import time


@overload(str)
def cm(command: str, shell: bool = True) -> Tuple[int, bytes, bytes]:
    if not isinstance(shell, bool):
        raise TypeError("In function 'cm' param 'shell' must be of type bool")
    res = subprocess.run(command.split(), shell=shell, capture_output=True)
    return res.returncode, res.stdout, res.stderr


@overload(list[str])
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
    res = subprocess.run(*args, shell=shell, capture_output=True)
    return res.returncode, res.stdout, res.stderr


def sleep(seconds: float):
    time.sleep(seconds)


def acm(command: str, inputs: list[str], i_timeout: float = 0.01, cwd=None, env=None, shell: bool = False, use_write_helper: bool = True) -> tuple[int, bytes | None, bytes | None]:
    """Advanced command

    Args:
        command (str): The command to execute
        inputs (list[str]): the inputs to give to the program from the command
        i_timeout (float, optional): An individual timeout for every step of the execution. Defaults to 0.01.
        cwd (_type_, optional): Current working directory. Defaults to None.
        env (_type_, optional): Environment variables. Defaults to None.
        shell (bool, optional): whether to execute the command through shell. Defaults to False.
        use_write_helper (bool, optional): whether to parse each input as it would have been parse with builtin print() or to use raw text. Defaults to True.

    Raises:
        If @timeout will raise something other than TimeoutError
        If the subprocess input and output handling will raise an exception

    Returns:
        tuple[int, bytes | None, bytes | None]: return code, stdout, stderr
    """
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, env=env, shell=shell)

        def write(*args, sep=" ", end="\n") -> None:
            b_args = str_to_bytes(sep).join(str_to_bytes(v) for v in args)
            b_end = str_to_bytes(end)
            p.stdin.write(b_args+b_end)
            p.stdin.flush()

        @timeout(i_timeout)
        def readline(s: IO, l: list):
            l.extend([s.readline()])

        def extend_from_stream(s: IO[bytes], l: list):
            if s is not None and s.readable():
                while True:
                    try:
                        readline(s, l)
                    except TimeoutError:
                        break
                    except BaseException as e1:
                        raise e1

        stdout: list = []
        stderr: list = []
        for input in inputs:
            if p.stdin.writable():
                if use_write_helper:
                    write(input)
                else:
                    write(input, sep="", end="")
            extend_from_stream(p.stdout, stdout)
            extend_from_stream(p.stderr, stderr)

        p.stdin.close()
        p.stdout.close()
        if p.stderr is not None:
            p.stderr.close()
        returncode = p.wait()
        return returncode, b"".join(stdout), stderr
    except BaseException as e2:
        raise e2
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
