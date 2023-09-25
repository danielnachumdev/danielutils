from typing import Optional, IO
from .decorators.validate import validate


RESET = "\033[0m"


class ColoredText:
    """static utility class with static functions:\n
        from_rgb,
        green,
        red,
        blue,
        red,
        yellow,
        white,
        black
    """
    @staticmethod
    @validate
    def from_rgb(red: int, green: int, blue: int, text: str) -> str:
        """Applies an RGB color to the given text.

        Args:
            r (int): The red component of the color.
            g (int): The green component of the color.
            b (int): The blue component of the color.
            text (str): The text to apply the color to.

        Returns:
            str: The given text with an RGB color applied to it.
        """
        return f"\033[38;2;{red};{green};{blue}m{text}{RESET}"

    @staticmethod
    def green(text: str) -> str:
        """Applies green color to the given text.

        Args:
            text (str): The text to apply the green color to.

        Returns:
            str: The given text with green color applied to it.
        """
        return ColoredText.from_rgb(0, 255, 0, text)

    @staticmethod
    def blue(text: str):
        """Applies blue color to the given text.

        Args:
            text (str): The text to apply the blue color to.

        Returns:
            str: The given text with blue color applied to it.
        """
        return ColoredText.from_rgb(0, 0, 255, text)

    @staticmethod
    def red(text: str):
        """Applies red color to the given text.

        Args:
            text (str): The text to apply the red color to.

        Returns:
            str: The given text with red color applied to it.
        """
        return ColoredText.from_rgb(255, 0, 0, text)

    @staticmethod
    def yellow(text: str):
        """Applies yellow color to the given text.

        Args:
            text (str): The text to apply the yellow color to.

        Returns:
            str: The given text with yellow color applied to it.
        """
        return ColoredText.from_rgb(255, 255, 0, text)

    @staticmethod
    def orange(text: str):
        """Applies yellow color to the given text.

        Args:
            text (str): The text to apply the yellow color to.

        Returns:
            str: The given text with yellow color applied to it.
        """
        return ColoredText.from_rgb(255, 165, 0, text)

    @staticmethod
    def white(text: str):
        """Applies white color to the given text.

        Args:
            text (str): The text to apply the white color to.

        Returns:
            str: The given text with white color applied to it.
        """
        return ColoredText.from_rgb(255, 255, 255, text)

    @staticmethod
    def black(text: str):
        """Applies black color to the given text.

        Args:
            text (str): The text to apply the black color to.

        Returns:
            str: The given text with black color applied to it.
        """
        return ColoredText.from_rgb(0, 0, 0, text)

    @staticmethod
    def supports_color(stream: IO) -> bool:
        """return whether a stream will support colored text

        Args:
            stream (IO): stream to check

        Returns:
            bool: boolean result
        """
        return stream.isatty()


def __special_print(*args, sep: str = " ", end: str = "\n", start_with: Optional[str] = None):
    """inner helper function"""
    if start_with:
        if "\n" not in sep:
            print(f"{start_with}: ", end="")
            print(sep.join([str(arg) for arg in args]), sep="", end=end)
        else:
            print(
                sep.join([f"{start_with}: {str(arg)}" for arg in args]), sep="", end=end)
    else:
        print(*args, sep=sep, end=end)


def success(*args, sep: str = " ", end: str = "\n"):
    """print a success message

    Args:
        sep (str, optional): print separator. Defaults to " ".
        end (str, optional): print endline. Defaults to "\\n".
    """

    __special_print(*args, sep=sep, end=end,
                    start_with=ColoredText.green("SUCCESS"))


def warning(*args, sep: str = " ", end: str = "\n"):
    """print a warning message

    Args:
        sep (str, optional): print separator. Defaults to " ".
        end (str, optional): print endline. Defaults to "\\n".
    """

    __special_print(*args, sep=sep, end=end,
                    start_with=ColoredText.orange("WARNING"))


def error(*args, sep: str = " ", end: str = "\n"):
    """print an error message

    Args:
        sep (str, optional): print separator. Defaults to " ".
        end (str, optional): print endline. Defaults to "\\n".
    """
    __special_print(*args, sep=sep, end=end,
                    start_with=ColoredText.red("ERROR"))


def info(*args, sep: str = " ", end: str = "\n"):
    """print an error message

    Args:
        sep (str, optional): print separator. Defaults to " ".
        end (str, optional): print endline. Defaults to "\\n".
    """
    __special_print(*args, sep=sep, end=end,
                    start_with=ColoredText.yellow("INFO"))


__all__ = [
    "ColoredText",
    "success",
    "warning",
    "error",
    "info"
]
