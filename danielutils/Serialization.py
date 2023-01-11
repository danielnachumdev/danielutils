from .Decorators import overload
import json


class Serializable:
    IDENTIFIER_LABEL = "__IDENTIFIER__"

    def __init__(self):
        pass

    def to_json(self):
        return self.__dict__

    def serialize(self, path: str, JSON: bool = True) -> str:
        d = self.__dict__
        d[Serializable.IDENTIFIER_LABEL] = f"{type(self).__module__}.{type(self).__qualname__}"
        with open(path, "w") as file:
            file.write(json.dumps(
                self, default=lambda _: d, indent=4))

    @staticmethod
    def __static_deserialize(path: str, globals, JSON: bool = True):
        with open(path, "r") as file:
            d = json.loads(file.read())
            type_name = d[Serializable.IDENTIFIER_LABEL]
            classes = [v for v in globals]
            return d

    @classmethod
    def deserialize(cls, path: str, globals=None, JSON: bool = True):
        if cls == Serializable:
            return Serializable.__static_deserialize(path, globals, JSON)
        return Serializable.__class_deserialize(cls, path, JSON)

    def __class_deserialize(cls, path: str, JSON: bool = True):
        with open(path, "r") as file:
            d = json.loads(file.read())
            # res = cls
            # res.__dict__ = d
            return d


__all__ = [
    # "Serializable"
]
