import os
from .Decorators import validate


@validate(str, list)
def write_to_file(path: str, lines: list[str]) -> None:
    """clear and then write data to file

    Args:
        path (str): path of file
        lines (list[str]): data to write
    """
    with open(path, "w") as f:
        for line in lines:
            f.write(line)


@validate(str)
def file_exists(path: str) -> bool:
    """checks wheter a file exists

    Args:
        path (str): path to check

    Returns:
        bool: result of check
    """
    return os.path.exists(path)


@validate(str)
def delete_file(path: str) -> None:
    """deletes a file if it exists

    Args:
        path (str): path of file
    """
    if file_exists(path):
        os.remove(path)
