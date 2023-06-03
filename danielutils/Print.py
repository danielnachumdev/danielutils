import sys
from .Functions.areoneof import areoneof
from .Math.MathPrint import mprint_parse_one
from .Decorators import atomic, deprecate


def mprint(*args, sep: str = " ", end: str = "\n", stream=sys.stdout) -> None:
    """Prints a formatted representation of mathematical expressions to the specified stream.

    Args:
        *args: The mathematical expressions to print.
        sep (str, optional): The separator to use between the expressions. Defaults to " ".
        end (str, optional): The string to append to the end of the printed expressions. Defaults to "\n".
        stream (file object, optional): The stream to write the output to. Defaults to sys.stdout.

    Raises:
        TypeError: If any of the arguments is not a string.

    Returns:
        None
    """
    if not areoneof(args, [str]):
        raise TypeError("s must be a string")
    stream.write(sep.join([mprint_parse_one(s) for s in args])+end)


@deprecate("The built-in 'print' function has an argument called 'file', use this instead")
def sprint(*args, sep: str = " ", end: str = "\n", stream=sys.stdout) -> None:
    """Writes a string representation of the given arguments to the specified stream.

    Args:
        *args: The arguments to print.
        sep (str, optional): The separator to use between the arguments. Defaults to " ".
        end (str, optional): The string to append to the end of the printed arguments. Defaults to "\n".
        stream (file object, optional): The stream to write the output to. Defaults to sys.stdout.

    Returns:
        None
    """
    stream.write(sep.join(args)+end)


@atomic
def aprint(*args, sep=" ", end="\n") -> None:
    """Prints a string representation of the given arguments to the console.

    Args:
        *args: The arguments to print.
        sep (str, optional): The separator to use between the arguments. Defaults to " ".
        end (str, optional): The string to append to the end of the printed arguments. Defaults to "\n".

    Returns:
        None
    """
    print(*args, sep=sep, end=end)


@atomic
def bprint(*args, sep=" ", end="\n", stream=sys.stdout) -> None:
    """A function that writes a string representation of the given arguments to the specified stream.

    Args:
        *args: The arguments to print.
        sep (str, optional): The separator to use between the arguments. Defaults to " ".
        end (str, optional): The string to append to the end of the printed arguments. Defaults to "\n".
        stream (file object, optional): The stream to write the output to. Defaults to sys.stdout.

    Returns:
        None
    """
    stream.write(sep.join(args)+end)


__all__ = [
    "sprint",
    "mprint",
    "aprint",
    "bprint"
]
