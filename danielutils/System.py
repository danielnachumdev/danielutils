from .Decorators import overload
from typing import Tuple, Union
import subprocess


@overload(str)
def cm(command: str, shell: bool = True) -> Tuple[int, bytes, bytes]:
    if not isinstance(shell, bool):
        raise TypeError("In function 'cm' param 'shell' must be of type bool")
    res = subprocess.run(command.split(), shell=shell, capture_output=True)
    return res.returncode, res.stdout, res.stderr


@overload(list[str])
def cm(*args, shell: bool = True) -> Tuple[int, bytes, bytes]:
    """exceute windows shell command and return output

    Args:
        command or args:\n
        command (str): A string representation of the command to exceute.
        args (list[str]): A list of all the command parts
        shell (bool, optional): whether to exceute in shell. Defaults to True.

    Raises:
        TypeError: wiil raise if 'shell' is not boolean

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
