import logging
from .logging_.utils import get_logger

logger = get_logger(__name__)


def singleton(og_class):
    """Decorator that ensures a class has only one instance (Singleton pattern)."""
    instance = None
    original_new = getattr(og_class, '__new__')
    original_init = getattr(og_class, '__init__')

    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            logger.debug(f"Creating singleton instance for {og_class.__name__}")
            # index 0 is the current class.
            # in the minimal case index 1 has 'object' class
            # otherwise the immediate parent of current class
            cls_index, og_index = 0, list(cls.__mro__).index(og_class)
            blacklist = {*cls.__mro__[:og_index + 1]}
            for candidate in cls.__mro__[og_index + 1:]:
                if candidate not in blacklist:
                    try:
                        instance = candidate.__new__(cls, *args, **kwargs)
                        logger.debug(f"Successfully created singleton instance using {candidate.__name__}")
                        break
                    except Exception as e:
                        logger.debug(f"Failed to create instance using {candidate.__name__}: {e}")
                        pass
            else:
                instance = object.__new__(cls)
                logger.debug(f"Created singleton instance using object.__new__")
        else:
            logger.debug(f"Returning existing singleton instance for {og_class.__name__}")
        return instance

    is_init: bool = False

    def __init__(self, *args, **kwargs) -> None:
        nonlocal is_init
        if not is_init:
            logger.debug(f"Initializing singleton instance for {og_class.__name__}")
            original_init(self, *args, **kwargs)
            is_init = True
            logger.info(f"Singleton instance initialized for {og_class.__name__}")
        else:
            logger.debug(f"Singleton instance already initialized for {og_class.__name__}")

    setattr(og_class, "__new__", __new__)
    setattr(og_class, "__init__", __init__)
    setattr(og_class, "instance", lambda: instance)
    logger.debug(f"Applied singleton decorator to {og_class.__name__}")
    return og_class


__all__ = [
    "singleton"
]
