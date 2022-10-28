from .Decorators import overload
from .Typing import Tuple, Union
import subprocess


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


__all__ = [
    "cm"
]
