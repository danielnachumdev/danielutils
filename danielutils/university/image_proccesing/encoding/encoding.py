from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable, Generator, Union

Encodeable = Union[bytes, Iterable[bytes]]
Decodeable = Encodeable


class Encoding(ABC):
    class EncodingType(Enum):
        LOSSY = "LOSSY"
        LOSSLESS = "LOSSLESS"

    encoding_type: EncodingType

    @staticmethod
    @abstractmethod
    def encode_online(obj: Encodeable) -> Generator[bytes, None, None]: ...

    @staticmethod
    @abstractmethod
    def encode_offline(obj: Encodeable) -> bytes: ...

    @staticmethod
    @abstractmethod
    def decode_online(obj: Decodeable) -> Generator[bytes, None, None]: ...

    @staticmethod
    @abstractmethod
    def decode_offline(obj: Decodeable) -> bytes: ...


__all__ = [
    'Encoding'
]
