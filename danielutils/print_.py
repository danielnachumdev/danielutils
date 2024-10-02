import sys
from typing import IO, List
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


@deprecate("The built-in 'print' function has an argument called 'file', use this instead")  # type:ignore
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


@atomic  # type:ignore
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
    def __init__(self, stream: IO = sys.stdout, thread_safe: bool = False):
        self.stream: IO = stream
        if thread_safe:
            self.__call__ = atomic(self.__call__)  # type:ignore
        self._current_row: int = 0
        self.rows: List[str] = []

    def clear(self, flush: bool = True) -> None:
        if not self.stream.isatty():
            warning(f"Cannot clear because {self.stream} is not a terminal stream")
            return
        self.write("\033[2J", flush=flush)
        self.rows.pop()

    def clear_line(self) -> None:
        self.write("\033[2K", end="")
        self.rows.pop()

    def move_up(self, num_lines: int = 1) -> None:
        self.write(f"\033[{num_lines}A", end="")
        self.rows.pop()
        self._current_row -= 1

    def write(self, *args, sep: str = " ", end: str = "\n", flush: bool = True):
        text = sep.join(args) + end
        self._current_row += text.count("\n")
        self.rows.extend([f"{s}\n" for s in text.splitlines() if len(s) > 0])
        self.stream.write(text)
        if flush:
            self.stream.flush()

    def __call__(self, *args, sep: str = " ", end: str = "\n", flush: bool = True) -> None:
        self.write(*args, sep=sep, end=end, flush=flush)

    @property
    def current_row(self) -> int:
        return self._current_row

    def insert(self, text: str, row: int) -> None:
        for _ in range(len(self.rows)):
            bprint.move_up()
            bprint.clear_line()
        self.rows.insert(row, text)
        num = len(self.rows)
        self.write(*self.rows, end="")
        for _ in range(num):
            self.rows.pop()


bprint = BetterPrinter()

__all__ = [
    "sprint",
    "mprint",
    "aprint",
    "bprint",
    'BetterPrinter'
]
