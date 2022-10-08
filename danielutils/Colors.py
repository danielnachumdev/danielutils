from .Decorators import validate


class ColoredText:
    __rgb_validateion = [int, lambda v: 0 <=
                         v <= 255, "rgb value must be in [0,255]"]

    @staticmethod
    @validate(__rgb_validateion, __rgb_validateion, __rgb_validateion, str)
    def from_rgb(r: int, g: int, b: int, text: str):
        return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"

    @staticmethod
    def green(text: str):
        return ColoredText.from_rgb(0, 255, 0, text)

    @staticmethod
    def blue(text: str):
        return ColoredText.from_rgb(0, 0, 255, text)

    @staticmethod
    def red(text: str):
        return ColoredText.from_rgb(255, 0, 0, text)

    @staticmethod
    def yellow(text: str):
        return ColoredText.from_rgb(255, 255, 0, text)

    @staticmethod
    def white(text: str):
        return ColoredText.from_rgb(255, 255, 255, text)

    @staticmethod
    def black(text: str):
        return ColoredText.from_rgb(0, 0, 0, text)


def __special_print(*args, sep=" ", end="\n", start_with=None):
    if start_with:
        if "\n" not in sep:
            print(f"{start_with}: ", end="")
            print(sep.join([arg for arg in args]), sep="", end=end)
        else:
            print(
                sep.join([f"{start_with}: {arg}" for arg in args]), sep="", end=end)
    else:
        print(*args, sep=sep, end=end)


def warning(*args, sep=" ", end="\n"):
    """print a warning message

    Args:
        sep (str, optional): print seperator. Defaults to " ".
        end (str, optional): print endline. Defaults to "\\n".
    """

    __special_print(*args, sep=sep, end=end,
                    start_with=ColoredText.yellow("WARNING"))


def error(*args, sep=" ", end="\n"):
    """print an error message

    Args:
        sep (str, optional): print seperator. Defaults to " ".
        end (str, optional): print endline. Defaults to "\\n".
    """
    __special_print(*args, sep=sep, end=end,
                    start_with=ColoredText.red("ERROR"))


__all__ = [
    "ColoredText",
    "warning",
    "error"
]
