import logging
from typing import Protocol, runtime_checkable, Any
from ..logging_.utils import get_logger

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
    logger.info("Serializing object of type: %s", type(obj).__name__)
    if isinstance(obj, Serializable):
        result = obj.serialize()
        logger.info("Serialization successful, returned %s bytes", len(result))
        return result
    logger.warning("Object %s does not implement Serializable protocol", type(obj).__name__)
    #TODO
    return b""


def deserialize(obj: bytes) -> Any:
    logger.info("Deserializing %s bytes", len(obj))
    logger.warning("Deserialize function not implemented (TODO)")
    #TODO
    return None


__all__ = [
    'Serializable',
    'serialize',
    'deserialize',
]
