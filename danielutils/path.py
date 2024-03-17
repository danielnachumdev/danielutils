import os


def get_current_working_directory() -> str:
    """return the current working directory

    Returns:
        str: current working directory
    """
    return os.getcwd()


def set_current_working_directory(path: str) -> None:
    """sets the current working directory

    Args:
        path (str): directory to set to
    """
    os.chdir(path)


def get_absolute_path(path: str) -> str:
    """return the absolute path of given path

    Args:
        path (str): a path

    Returns:
        str: absolute version of that path
    """
    return os.path.abspath(path)


def get_relative_path(path: str) -> str:
    """return the relative path of given path

    Args:
        path (str): a path

    Returns:
        str: relative (to current working directory) version of that path
    """
    return os.path.realpath(path)


__all__ = [
    "get_current_working_directory",
    "set_current_working_directory",
    "get_absolute_path",
    "get_relative_path"
]
