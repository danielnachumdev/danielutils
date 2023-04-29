# -*- coding: utf-8 -*-
import subprocess
from typing import IO, Iterator, Generator
import shutil
from pathlib import Path
import os
from .Decorators import validate


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
            raise UnicodeDecodeError(
                "Can't read byte in file.\nTo use with bytes use: read_bytes = True ") from e
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
    """clears the content of a directory

    Args:
        path (str): the path of the directory to clean
    """
    for file in get_files(path):
        delete_file(f"{path}\\{file}")
    for subdir in get_directories(path):
        delete_directory(f"{path}\\{subdir}")


@validate
def create_directory(path: str) -> None:
    """create a directory at the specified path if it doesn't already exists

    Args:
        path (str): the path to create a directory at
    """
    if not directory_exists(path):
        os.makedirs(path)


@validate
def get_file_type_from_directory(path: str, file_type: str) -> Iterator[str]:
    """returns all file with specific type from a directory

    Args:
        path (str): path of directory
        file_type (str): the desired file type. eg: ".png"

    Returns:
        list[str]: result
    """
    return filter(
        lambda name: Path(f"{path}\\{name}").suffix == file_type,
        get_files(path)
    )


@validate
def get_file_type_from_directory_recursively(path: str, file_type: str) -> Generator[str, None, None]:
    """_summary_

    Args:
        path (str): _description_
        file_type (str): _description_

    Returns:
        _type_: _description_
    """
    yield from filter(
        lambda name: Path(f"{path}\\{name}").suffix == file_type,
        get_files(path)
    )
    for subdir in get_directories(path):
        for v in get_file_type_from_directory_recursively(f"{path}\\{subdir}", file_type):
            yield f"{subdir}\\{v}"


def rename_file(path: str, new_name: str) -> None:
    """renames a file

    Args:
        path (str): file to rename
        new_name (str): the desired new name
    """
    new_path = "./" + \
        "/".join(Path(path).parts[:-1])+"/"+new_name+Path(path).suffix
    move_file(path, new_path)


def move_file(old_path: str, new_path: str) -> None:
    """moves a file

    Args:
        old_path (str): old path
        new_path (str): new path
    """
    os.rename(old_path, new_path)


async def open_file(file_path: str, application_path: str) -> int:
    """open a file with the specified application

    Args:
        file_path (str): the file to open
        application_path (str): the application to open with
    Returns:
        int: return code
    """
    with subprocess.Popen([application_path, file_path]) as p:
        return p.wait()


def move_directory(old_path: str, new_path: str) -> None:
    """moves a directory

    Args:
        old_path (str): old path
        new_path (str): new path
    """
    shutil.move(old_path, new_path)


def copy_file(src: str, dest: str) -> None:
    """copies file from src to dest

    Args:
        src (str): src
        dest (str): dest
    """
    shutil.copy(src, dest)


def copy_directory(src: str, dest: str) -> None:
    """copies a directory from src to dest

    Args:
        src (str): stc
        dest (str): dest
    """
    shutil.copy(src, dest)


class IndentedWriter:
    """every class that will inherit this class will have the following functions available
        write() with the same arguments a builtin print()
        indent()
        undent()

        also, it is expected in the __init__ function to call super().__init__()
        also, the output_stream must be set whether by the first argument io super().__init__(...)
        or by set_stream() explicitly somewhere else.

        this class will not function properly is the output_stream is not set!

    """

    def __init__(self, output_stream: IO = None, indent_value: str = "\t"):
        self.indent_level = 0
        self.output_stream: IO = output_stream
        self.indent_value = indent_value

    def write(self, *args, sep=" ", end="\n"):
        """writes the supplied arguments to the output_stream

        Args:
            sep (str, optional): the str to use as a separator between arguments. Defaults to " ".
            end (str, optional): the str to use as the final value. Defaults to "\n".

        Raises:
            ValueError: _description_
        """
        if self.output_stream is None:
            raise ValueError(
                "Can't write to an empty stream. the stream must not be None: either by set_stream or by initialization")
        self.output_stream.write(
            str(self.indent_level*self.indent_value + sep.join(args)+end))

    def set_stream(self, stream: IO):
        """explicitly sets the stream

        Args:
            stream (IO): stream
        """
        self.output_stream = stream

    def indent(self) -> None:
        """indents the preceding output with write() by one quantity more
        """
        self.indent_level += 1

    def undent(self) -> None:
        """un-dents the preceding output with write() by one quantity less
            has a minimum value of 0
        """
        self.indent_level = max(0, self.indent_level-1)


__all__ = [
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
