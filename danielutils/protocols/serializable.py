from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> bytes: ...

    def deserialize(self, serealized: bytes) -> 'Serializable': ...


def serialize(obj: Any) -> bytes:
    if isinstance(obj, Serializable):
        return obj.serialize()

    pass


def deserialize(obj: bytes) -> Any:
    if isinstance(obj, Serializable):
        return obj.deserialize()
    pass


__all__ = [
    'Serializable',
    'serialize',
    'deserialize',
]
