# -*- coding: utf-8 -*-
from typing import IO
import shutil
import os
from .Decorators import validate
from typing import Union
from pathlib import Path


@validate
def write_to_file(path: str, lines: Union[list[str], list[bytes]], write_bytes: bool = False) -> None:
    """clear and then write data to file

    Args:
        path (str): path of file
        lines (list[str]): data to write
    """

    try:
        if write_bytes:
            with open(path, "wb") as f:
                f.writelines(lines)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(lines)
    except Exception as e:
        if isinstance(e, TypeError):
            raise Exception(
                "'lines' contains a 'bytes' object.\nTo use with bytes use: write_bytes = True ")
        raise e


@validate
def path_exists(path: str) -> bool:
    """checks whether a path exists

    Args:
        path (str): path to check

    Returns:
        bool: result of check
    """
    return os.path.exists(path)


@validate
def file_exists(path: str) -> bool:
    """checks whether a file exists at specified path

    Args:
        path (str): path to check

    Returns:
        bool: will return true iff the path exists and it is a path to a file
    """
    return path_exists(path) and is_file(path)


@validate
def directory_exists(path: str) -> bool:
    """checks whether a directory exists at specified path

    Args:
        path (str): path to check

    Returns:
        bool: will return true iff the path exists and it is a path to a directory
    """
    return path_exists(path) and is_directory(path)


@validate
def delete_file(path: str) -> None:
    """deletes a file if it exists

    Args:
        path (str): path of file
    """
    if file_exists(path):
        os.remove(path)


@validate
def read_file(path: str, read_bytes: bool = False) -> list[str]:
    """read all lines from a file

    Args:
        path (str): the path to the file

    Returns:
        list[str]: a list of all the lines in the file
    """
    try:
        if read_bytes:
            with open(path, "rb") as f:
                return f.readlines()
        else:
            with open(path, "r", encoding="mbcs") as f:
                return f.readlines()
    except Exception as e:
        if isinstance(e, UnicodeDecodeError):
            raise Exception(
                f"Can't read byte in file.\nTo use with bytes use: read_bytes = True ")
        raise e


@validate
def is_file(path: str) -> bool:
    """return whether a path represents a file

    Args:
        path (str): path to check
    """
    return os.path.isfile(path)


@validate
def is_directory(path: str) -> bool:
    """return whether a path represents a directory

    Args:
        path (str): path to check
    """
    return os.path.isdir(path)


@validate
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


@validate
def get_files_and_directories(path: str) -> list[str]:
    """get a list of all files and directories in specified path

    Args:
        path (str): path to check

    Returns:
        list[str]: all files and directories
    """
    return os.listdir(path)


@validate
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


@ validate
def delete_directory(path: str) -> None:
    """delete a directory and all its contents

    Args:
        path (str): _description_
    """
    if is_directory(path):
        clear_directory(path)
        os.rmdir(path)


@validate
def clear_directory(path: str) -> None:
    for file in get_files(path):
        delete_file(f"{path}\\{file}")
    for dir in get_directories(path):
        delete_directory(f"{path}\\{dir}")


@validate
def create_directory(path: str) -> None:
    """create a directory at the specified path if it doesn't already exists

    Args:
        path (str): the path to create a directory at
    """
    if not directory_exists(path):
        os.makedirs(path)


@validate
def get_file_type_from_directory(path: str, file_type: str) -> list[str]:
    return list(
        filter(
            lambda name: Path(f"{path}\\{name}").suffix == file_type,
            get_files(path)
        )
    )


@validate
def get_file_type_from_directory_recursively(path: str, file_type: str):
    res = []
    for dir in get_directories(path):
        res.extend(f"{dir}\\{v}" for v in get_file_type_from_directory_recursively(
            f"{path}\\{dir}", file_type))
    res.extend(list(
        filter(
            lambda name: Path(f"{path}\\{name}").suffix == file_type,
            get_files(path)
        )
    ))
    return res


def rename_file(path: str, new_name: str) -> None:
    new_path = "./" + \
        "/".join(Path(path).parts[:-1])+"/"+new_name+Path(path).suffix
    move_file(path, new_path)


def move_file(old_path: str, new_path: str) -> None:
    os.rename(old_path, new_path)


async def open_file(file_path: str, application_path: str):
    import subprocess
    p = subprocess.Popen([application_path, file_path])
    return_code = p.wait()


def move_directory(old_path: str, new_path: str) -> None:
    shutil.move(old_path, new_path)


def copy_file(src: str, dest: str) -> None:
    shutil.copy(src, dest)


def copy_directory(src: str, dest: str) -> None:
    shutil.copy(src, dest)


class IndentedWriter:
    def __init__(self, output_stream: IO, indent_char: str = "\t"):
        self.indent_level = 0
        self.output_stream: IO = output_stream
        self.indent_char = indent_char

    def write(self, *args, sep=" ", end="\n"):
        self.output_stream.write(
            self.indent_level*self.indent_char + sep.join(args)+end)

    def indent(self):
        self.indent_level += 1

    def undent(self):
        self.indent_level = max(0, self.indent_level-1)


__all__ = [
    "write_to_file",
    "path_exists",
    "file_exists",
    "directory_exists",
    "delete_file",
    "read_file",
    "is_file",
    "is_directory",
    "get_files",
    "get_files_and_directories",
    "get_directories",
    "delete_directory",
    "clear_directory",
    "create_directory",
    "get_file_type_from_directory",
    "get_file_type_from_directory_recursively",
    "rename_file",
    "move_file",
    "open_file",
    "move_directory",
    "copy_file",
    "copy_directory",
    "IndentedWriter"
]
