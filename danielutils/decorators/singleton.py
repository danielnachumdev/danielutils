import logging
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def singleton(og_class):
    """Decorator that ensures a class has only one instance (Singleton pattern)."""
    instance = None
    original_new = getattr(og_class, '__new__')
    original_init = getattr(og_class, '__init__')

    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            logger.debug("Creating singleton instance for %s", og_class.__name__)
            # index 0 is the current class.
            # in the minimal case index 1 has 'object' class
            # otherwise the immediate parent of current class
            cls_index, og_index = 0, list(cls.__mro__).index(og_class)
            blacklist = {*cls.__mro__[:og_index + 1]}
            for candidate in cls.__mro__[og_index + 1:]:
                if candidate not in blacklist:
                    try:
                        instance = candidate.__new__(cls, *args, **kwargs)
                        logger.debug("Successfully created singleton instance using %s", candidate.__name__)
                        break
                    except Exception as e:
                        logger.debug("Failed to create instance using %s: %s", candidate.__name__, e)
                        pass
            else:
                instance = object.__new__(cls)
                logger.debug("Created singleton instance using object.__new__")
        else:
            logger.debug("Returning existing singleton instance for %s", og_class.__name__)
        return instance

    is_init: bool = False

    def __init__(self, *args, **kwargs) -> None:
        nonlocal is_init
        if not is_init:
            logger.debug("Initializing singleton instance for %s", og_class.__name__)
            original_init(self, *args, **kwargs)
            is_init = True
            logger.info("Singleton instance initialized for %s", og_class.__name__)
        else:
            logger.debug("Singleton instance already initialized for %s", og_class.__name__)

    setattr(og_class, "__new__", __new__)
    setattr(og_class, "__init__", __init__)
    setattr(og_class, "instance", lambda: instance)
    logger.debug("Applied singleton decorator to %s", og_class.__name__)
    return og_class


__all__ = [
    "singleton"
]
