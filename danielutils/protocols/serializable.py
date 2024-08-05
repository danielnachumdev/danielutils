from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> bytes: ...

    def deserialize(self, serealized: bytes) -> 'Serializable': ...


def serialize(obj: Any) -> bytes:
    if isinstance(obj, Serializable):
        return obj.serialize()
    #TODO
    return b""


def deserialize(obj: bytes) -> Any:
    #TODO
    return None


__all__ = [
    'Serializable',
    'serialize',
    'deserialize',
]
