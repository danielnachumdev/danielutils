from typing import Generator, Sequence, List
from .lossless_encoding import LosslessEncoding
from ..encoding import Decodeable, Encodeable


class RunLengthEncoding(LosslessEncoding):
    @staticmethod
    def encode_online(obj: Encodeable) -> Generator[bytes, None, None]:
        buffer: List[int] = []
        for c in obj:
            if len(buffer) > 0:
                if c != buffer[0]:
                    yield chr(buffer[0]).encode() + str(len(buffer)).encode()
                    buffer.clear()
            buffer.append(c)
        yield chr(buffer[0]).encode() + str(len(buffer)).encode()

    @staticmethod
    def decode_online(obj: Decodeable) -> Generator[bytes, None, None]:
        raise NotImplementedError("RunLengthEncoding.decode_online() is not implemented")

    SEPERATOR = b","
