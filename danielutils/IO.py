import os
from .Decorators import validate
from typing import Union


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


@validate(str)
def read_file(path: str) -> list[str]:
    """read all lines from a file

    Args:
        path (str): the path to the file

    Returns:
        list[str]: a list of all the lines in the file
    """
    with open(path, "r", encoding="utf8") as txt_file:
        return txt_file.readlines()


@validate(str)
def is_file(path: str) -> bool:
    """return wheter a path represents a file

    Args:
        path (str): path to checl
    """
    return os.path.isfile(path)


@validate(str)
def is_directory(path: str) -> bool:
    """return wheter a path represents a directory

    Args:
        path (str): path to checl
    """
    return os.path.isdir(path)


# @validate(str)
# def get_files(path: str) -> list[str]:
#     if is_directory(path):
#         pass


# @validate(str)
# def get_directories(path: str) -> list[str]:
#     if is_directory(path):
#         pass


# @ validate(str)
# def delete_directory(path: str) -> None:
#     """delete a directory and all its contents

#     Args:
#         path (str): _description_
#     """
#     if is_directory(path):
#         for dir in get_directories(path):
#             delete_directory(f"{path}\\{dir}")
#         for file in get_files(dir):
#             delete_file(file)
