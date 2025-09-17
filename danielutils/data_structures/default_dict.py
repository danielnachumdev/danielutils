import logging
from danielutils.logging_.utils import get_logger
from .logging_.utils import get_logger
logger = get_logger(__name__)


class DefaultDict(dict):
    """
    My implementation to `collections.defaultdict`
    """

    def __init__(self, cls):
        self._cls = cls
        logger.debug(f"DefaultDict initialized with default factory: {cls}")

    def __getitem__(self, key):
        if key not in self:
            logger.debug(f"Key '{key}' not found, creating default value using {self._cls}")
        return super().get(key, self._cls())


__all__ = [
    "DefaultDict"
]
