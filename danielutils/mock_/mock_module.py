import logging
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class MockImportObject:
    """
    A class to create a mock object that will raise an import error when you try to interact with it in some way
    """

    def __init__(self, msg: str):
        logger.info(f"Initializing MockImportObject with message: {msg}")
        self._msg = msg

    def __getattr__(self, item):
        logger.warning(f"MockImportObject attribute access blocked: {item} - {self._msg}")
        raise ImportError(self._msg)

    def __call__(self, *args, **kwargs):
        logger.warning(f"MockImportObject call blocked with {len(args)} args and {len(kwargs)} kwargs - {self._msg}")
        raise ImportError(self._msg)


__all__ = [
    "MockImportObject"
]
