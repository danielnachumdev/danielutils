import logging
import platform
from ..logging_.utils import get_logger
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def _get_python_version_untyped() -> tuple:
    values = (int(v) for v in platform.python_version().split("."))
    version = tuple(values)  # type:ignore
    return version


if _get_python_version_untyped() < (3, 9):
    from typing import Tuple as Tuple
else:
    from builtins import tuple as Tuple  # type:ignore


def get_python_version() -> Tuple[int, int, int]:
    """return the version of python that is currently running this code

    Returns:
        tuple[int, int, int]: version
    """
    version = _get_python_version_untyped()
    logger.info(f"Python version: {version}")
    return version  # type:ignore


__all__ = [
    "get_python_version"
]
