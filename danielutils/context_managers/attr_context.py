import logging
from typing import ContextManager
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class AttrContext(ContextManager):
    def __init__(self, obj: object, attr: str, new_value: object, *, nonexistent_is_error: bool = True) -> None:
        logger.debug("Initializing AttrContext for %s.%s = %s", type(obj).__name__, attr, new_value)
        self.obj = obj
        self.attr = attr
        self.new_value = new_value
        self.old_value = None
        self._has_attr: bool = hasattr(self.obj, self.attr)
        if nonexistent_is_error and not self._has_attr:
            logger.error("Attribute '%s' does not exist on %s", self.attr, type(obj).__name__)
            raise RuntimeError(f"Nonexistent attribute '{self.attr}' in '{self.obj}'")
        logger.debug("AttrContext initialized successfully, has_attr=%s", self._has_attr)

    def __enter__(self) -> 'AttrContext':
        logger.debug("Entering AttrContext for %s.%s", type(self.obj).__name__, self.attr)
        self.old_value = getattr(self.obj, self.attr, None)
        setattr(self.obj, self.attr, self.new_value)
        logger.info("Attribute %s set to %s (was %s)", self.attr, self.new_value, self.old_value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Exiting AttrContext for %s.%s, exc_type=%s", type(self.obj).__name__, self.attr, exc_type)
        if self._has_attr:
            setattr(self.obj, self.attr, self.old_value)
            logger.info("Attribute %s restored to %s", self.attr, self.old_value)
        else:
            delattr(self.obj, self.attr)
            logger.info("Temporary attribute %s removed", self.attr)


__all__ = [
    'AttrContext'
]
