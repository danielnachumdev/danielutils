import os
from .Decorators import validate


@validate(str)
def cm(command: str) -> str:
    """exceute windows shell command and return output

    Args:
        command (str): command to execute

    Returns:
        str: command result
    """
    return os.popen(command).read()


__all__ = [
    "cm"
]
# def open_file(filepath: str):
#     subprocess.Popen(['start', filepath], shell=True)
