from .Attribute import Attribute


class Relation:
    def __init__(self, attributes: list[str]):
        self.attributes = [Attribute(s) for s in attributes]

    def __contains__(self, attribute) -> bool:
        if isinstance(attribute, Attribute):
            return attribute in self.attributes
        return False

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return self.__class__.__name__+str(self.attributes)

    def to_attribute(self) -> Attribute:
        res = self.attributes[0]
        for i in range(1, len(self.attributes)):
            res.union(self.attributes[i])
        return res


__all__ = [
    "Relation"
]
