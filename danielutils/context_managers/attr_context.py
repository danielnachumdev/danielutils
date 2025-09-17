import logging
from typing import ContextManager
from .logging_.utils import get_logger

logger = get_logger(__name__)


class AttrContext(ContextManager):
    def __init__(self, obj: object, attr: str, new_value: object, *, nonexistent_is_error: bool = True) -> None:
        logger.debug(f"Initializing AttrContext for {type(obj).__name__}.{attr} = {new_value}")
        self.obj = obj
        self.attr = attr
        self.new_value = new_value
        self.old_value = None
        self._has_attr: bool = hasattr(self.obj, self.attr)
        if nonexistent_is_error and not self._has_attr:
            logger.error(f"Attribute '{self.attr}' does not exist on {type(obj).__name__}")
            raise RuntimeError(f"Nonexistent attribute '{self.attr}' in '{self.obj}'")
        logger.debug(f"AttrContext initialized successfully, has_attr={self._has_attr}")

    def __enter__(self) -> 'AttrContext':
        logger.debug(f"Entering AttrContext for {type(self.obj).__name__}.{self.attr}")
        self.old_value = getattr(self.obj, self.attr, None)
        setattr(self.obj, self.attr, self.new_value)
        logger.info(f"Attribute {self.attr} set to {self.new_value} (was {self.old_value})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Exiting AttrContext for {type(self.obj).__name__}.{self.attr}, exc_type={exc_type}")
        if self._has_attr:
            setattr(self.obj, self.attr, self.old_value)
            logger.info(f"Attribute {self.attr} restored to {self.old_value}")
        else:
            delattr(self.obj, self.attr)
            logger.info(f"Temporary attribute {self.attr} removed")


__all__ = [
    'AttrContext'
]
