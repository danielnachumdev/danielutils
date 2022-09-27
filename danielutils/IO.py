# -*- coding: utf-8 -*-
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
    with open(path, "w", encoding="utf-8") as f:
        for i, line in enumerate(lines):
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


@validate(str)
def get_files(path: str) -> list[str]:
    """return a list of names of all files inside specified directory

    Args:
        path (str): directory

    Returns:
        list[str]: all files
    """
    files_and_directories = get_files_and_directories(path)
    return list(
        filter(lambda name: is_file(f"{path}\\{name}"), files_and_directories))


@validate(str)
def get_files_and_directories(path: str) -> list[str]:
    """get a list of all files and directories in specified path

    Args:
        path (str): path to check

    Returns:
        list[str]: all files and directories
    """
    return os.listdir(path)


@validate(str)
def get_directories(path: str) -> list[str]:
    """get all directories in specified path

    Args:
        path (str): path to check

    Returns:
        list[str]: all directories
    """
    files_and_directories = get_files_and_directories(path)
    return list(
        filter(lambda name: is_directory(f"{path}\\{name}"), files_and_directories))


@ validate(str)
def delete_directory(path: str) -> None:
    """delete a directory and all its contents

    Args:
        path (str): _description_
    """
    if is_directory(path):
        for dir in get_directories(path):
            delete_directory(f"{path}\\{dir}")
        for file in get_files(dir):
            delete_file(f"{path}\\{dir}")


@validate(str, str)
def get_file_type_from_directory(path: str, file_type: str) -> list[str]:
    from pathlib import Path
    return list(
        filter(
            lambda name: Path(f"{path}\\{name}").suffix == file_type,
            get_files(path)
        )
    )


@validate(str, str)
def get_file_type_from_directory_recursivly(path: str, file_type: str):
    from pathlib import Path
    res = []
    for dir in get_directories(path):
        res.extend(f"{dir}\\{v}" for v in get_file_type_from_directory_recursivly(
            f"{path}\\{dir}", file_type))
    res.extend(list(
        filter(
            lambda name: Path(f"{path}\\{name}").suffix == file_type,
            get_files(path)
        )
    ))
    return res
