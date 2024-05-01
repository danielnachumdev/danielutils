import sys
from typing import IO
from .functions.areoneof import areoneof
from .math_.math_print import mprint_parse_one
from .decorators import atomic, deprecate
from .colors import warning


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
    stream.write(sep.join([mprint_parse_one(s) for s in args]) + end)


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
    stream.write(sep.join(args) + end)


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


class BetterPrinter:
    def __init__(self, thread_safe: bool = False):
        if thread_safe:
            self.__call__ = atomic(self.__call__)
        self._current_row: int = 0
        self.rows: list[str] = []

    def clear(self, stream: IO = sys.stdout, flush: bool = True) -> None:
        if not stream.isatty():
            warning(f"Cannot clear because {stream} is not a terminal stream")
            return
        self.write("\033[2J", stream=stream, flush=flush)
        self.rows.pop()

    def clear_line(self) -> None:
        self.write("\033[2K", end="")
        self.rows.pop()

    def move_up(self, num_lines: int = 1) -> None:
        self.write(f"\033[{num_lines}A", end="")
        self.rows.pop()
        self._current_row -= 1

    def write(self, *args, sep: str = " ", end: str = "\n", stream: IO = sys.stdout, flush: bool = True):
        text = sep.join(args) + end
        self._current_row += text.count("\n")
        self.rows.extend([f"{s}\n" for s in text.splitlines() if len(s) > 0])
        stream.write(text)
        if flush:
            stream.flush()

    def __call__(self, *args, **kwargs) -> None:
        self.write(*args, **kwargs)

    @property
    def current_row(self) -> int:
        return self._current_row

    def insert(self, text: str, row: int) -> None:
        self.rows.insert(row, text)
        num_rows = len(self.rows)
        self.clear()
        self.write(*self.rows)
        for _ in range(num_rows):
            self.rows.pop()


bprint = BetterPrinter()

__all__ = [
    "sprint",
    "mprint",
    "aprint",
    "bprint",
    'BetterPrinter'
]
