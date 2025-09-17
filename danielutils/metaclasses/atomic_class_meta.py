import logging
from ..decorators import atomic
from .logging_.utils import get_logger

logger = get_logger(__name__)


class AtomicClassMeta(type):
    """will make all of the class's function atomic
    """
    def __new__(mcs, name, bases, namespace):
        logger.info(f"Creating atomic class: {name}")
        
        # Process class methods
        class_methods_processed = 0
        for k, v in namespace.items():
            if callable(v):
                namespace[k] = atomic(v)  # type:ignore
                class_methods_processed += 1
        
        # Process inherited methods
        inherited_methods_processed = 0
        for base in bases:
            for k, v in base.__dict__.items():
                if callable(v):
                    if k not in namespace:
                        namespace[k] = atomic(v)  # type:ignore
                        inherited_methods_processed += 1
        
        logger.info(f"AtomicClassMeta: {name} created with {class_methods_processed} class methods and {inherited_methods_processed} inherited methods made atomic")
        return super().__new__(mcs, name, bases, namespace)


__all__ = [
    "AtomicClassMeta"
]
