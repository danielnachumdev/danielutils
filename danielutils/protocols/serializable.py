import logging
from typing import Protocol, runtime_checkable, Any
from .logging_.utils import get_logger

logger = get_logger(__name__)


@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> bytes:
        """
        Serialize the object to bytes.
        
        Note: This is a protocol method. Implementations should add logging
        to track serialization operations.
        """
        ...

    def deserialize(self, serealized: bytes) -> 'Serializable':
        """
        Deserialize bytes back to a Serializable object.
        
        Note: This is a protocol method. Implementations should add logging
        to track deserialization operations.
        """
        ...


def serialize(obj: Any) -> bytes:
    logger.info(f"Serializing object of type: {type(obj).__name__}")
    if isinstance(obj, Serializable):
        result = obj.serialize()
        logger.info(f"Serialization successful, returned {len(result)} bytes")
        return result
    logger.warning(f"Object {type(obj).__name__} does not implement Serializable protocol")
    #TODO
    return b""


def deserialize(obj: bytes) -> Any:
    logger.info(f"Deserializing {len(obj)} bytes")
    logger.warning("Deserialize function not implemented (TODO)")
    #TODO
    return None


__all__ = [
    'Serializable',
    'serialize',
    'deserialize',
]
