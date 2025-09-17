import logging
from typing import IO, Optional, cast, Union, Generator, Tuple as Tuple, List as List
from pathlib import Path
import subprocess
import time
from ..decorators import timeout, validate
from ..conversions import str_to_bytes
from ..generators import join_generators, generator_from_stream
from ..reflection import get_python_version
from .logging_.utils import get_logger

logger = get_logger(__name__)

if get_python_version() >= (3, 9):
    from builtins import tuple as Tuple, list as List  # type:ignore


def cm(*args: str, shell: bool = True) -> Tuple[int, bytes, bytes]:
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
    logger.info(f"Executing command: {' '.join(args)} (shell={shell})")
    if not isinstance(shell, bool):
        logger.error("'shell' parameter must be of type bool")
        raise TypeError(
            "In function 'cm' param 'shell' must be of type bool")
    
    for i, arg in enumerate(args):
        path_obj = Path(args[i])
        if path_obj.is_file() or path_obj.is_dir():
            args = (*args[:i], f"\"{arg}\"", *args[i + 1:])
    
    command_str = " ".join(args)
    res = subprocess.run(command_str, shell=shell,
                         capture_output=True, check=False)
    logger.info(f"Command completed with return code: {res.returncode}")
    return res.returncode, res.stdout, res.stderr


@validate  # type:ignore
def sleep(seconds: Union[int, float]) -> None:
    """make current thread sleep

    Args:
        seconds (float): number of seconds to sleep

    Returns:
        None
    """
    time.sleep(seconds)


def __acm_write(*args, p: subprocess.Popen, sep=" ", end="\n") -> None:
    p.stdin = cast(IO[bytes], p.stdin)
    b_args = str_to_bytes(sep).join(str_to_bytes(v) for v in args)
    b_end = str_to_bytes(end)
    p.stdin.write(b_args + b_end)
    p.stdin.flush()


@validate  # type:ignore
def acm(command: str, inputs: Optional[List[str]] = None, i_timeout: float = 0.01,
        shell: bool = False, use_write_helper: bool = True, cwd: Optional[str] = None) \
        -> Tuple[int, Optional[List[bytes]], Optional[List[bytes]]]:
    """Advanced command

    Args:
        command (str): The command to execute\n
        inputs (list[str]): the inputs to give to the program from the command. Defaults to None.\n
        i_timeout (float, optional): An individual timeout for every step of the execution. Defaults to 0.01.\n
        cwd (?, optional): Current working directory. Defaults to None.\n
        env (?, optional): Environment variables. Defaults to None.\n
        shell (bool, optional): whether to execute the command through shell. Defaults to False.\n
        use_write_helper (bool, optional): whether to parse each input as it
        would have been parse with builtin print() or to use raw text. Defaults to True.

    Raises:
        If @timeout will raise something other than TimeoutError.\n
        If the subprocess input and output handling will raise an exception.

    Returns:
        tuple[int, Optional[list[bytes]], Optional[list[bytes]]]: return code, stdout, stderr
    """

    if inputs is None:
        inputs = []

    p = None
    try:
        # with subprocess.Popen(command, stdout=subprocess.PIPE,
        #                      stdin=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, shell=shell) as p:
        # TODO with ... as p:
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, shell=shell)
        p.stdin = cast(IO[bytes], p.stdin)
        p.stdout = cast(IO[bytes], p.stdout)
        p.stderr = cast(IO[bytes], p.stderr)

        @timeout(i_timeout)  # type:ignore
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

        stdout: List[bytes] = []
        stderr: List[bytes] = []
        for curr_input in inputs:
            if p.stdin.writable():
                if use_write_helper:
                    __acm_write(curr_input, p=p)
                else:
                    __acm_write(curr_input, p=p, sep="", end="")
            extend_from_stream(p.stdout, stdout)
            extend_from_stream(p.stderr, stderr)
        # else:
        #     extend_from_stream(p.stdout, stdout)
        #     extend_from_stream(p.stderr, stderr)
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


def cmrt(*args, shell: bool = True) -> Generator[Tuple[int, bytes], None, None]:
    """Executes a command and yields stdout and stderr in real-time.

    Args:
        shell (bool, optional): If True, the command is executed through the shell. Defaults to True.

    Raises:
        TypeError: if 'shell' is not boolean

    Yields:
        Generator[tuple[int, bytes], None, None]: the tuple yielded will contain the 'stream identifier'
            0 - stdout,
            1 - stderr
        and the actual value from the stream
    """
    if not isinstance(shell, bool):
        raise TypeError("The 'shell' parameter must be of type bool.")

    # Quote the arguments that represent file or directory paths.
    for i, arg in enumerate(args):
        path_obj = Path(args[i])
        if path_obj.is_file() or path_obj.is_dir():
            args = (*args[:i], f"\"{arg}\"", *args[i + 1:])

    # Join the arguments into a command string and execute the command.
    cmd = " ".join(args)

    with subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        combined = join_generators(  # type:ignore
            generator_from_stream(process.stdout),  # type:ignore
            generator_from_stream(process.stderr)   # type:ignore
        )  # type:ignore
        for tup in combined:
            yield tup


__all__ = [
    "cm",
    "acm",
    "sleep",
    "cmrt"
]
