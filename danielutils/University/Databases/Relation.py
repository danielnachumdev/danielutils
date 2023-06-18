from typing import ForwardRef, Generator, Iterable
from .Attribute import Attribute
from ...Functions import powerset
from ...Generators import generate_except
Ft = ForwardRef("FunctionalDependencyGroup")


class Relation:
    @classmethod
    def from_strings(cls, lst: Iterable[str]) -> "Relation":
        return cls([Attribute(s) for s in lst])

    def __init__(self, attributes: list[Attribute]):
        self.attributes = attributes

    def __contains__(self, attribute) -> bool:
        if isinstance(attribute, Attribute):
            return attribute in self.attributes
        return False

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return self.__class__.__name__+str(self.attributes)

    def to_attribute(self) -> Attribute:
        res = self.attributes[0].clone()
        for i in range(1, len(self.attributes)):
            res.update(self.attributes[i])
        return res

    def __iter__(self) -> Generator[Attribute, None, None]:
        yield from self.attributes

    def is_preserved_by(self, relations: list["Relation"], functional_dependencies: ForwardRef("FunctionalDependencyGroup")):
        for dep in functional_dependencies:
            if not dep.is_preserved_by(relations, functional_dependencies):
                return False
        return True

    def __len__(self) -> int:
        return len(self.attributes)

    def subsets(self) -> Generator[Attribute, None, None]:
        for tup in generate_except(powerset(self), lambda index, _: index == 0):
            res = tup[0]
            for attr in tup[1:]:
                res = res.union(attr)
            yield res

    def is_BCNF(self, F: Ft) -> bool:
        for f in F:
            X, Y = f.key, f.value
            if not (Y in X or self.is_superkey(X, F)):
                return False
        return True

    def is_3NF(self, F: Ft) -> bool:
        BCNF = True

    def is_key(self, X: Attribute, F: Ft) -> bool:
        if not self.is_superkey(X, F):
            return False
        R = self.to_attribute()

        def subsets_of(X):
            for tup in generate_except(powerset(X), lambda _, v: len(v) in {0, len(X)}):
                Y = tup[0]
                for Y_ in tup[1:]:
                    Y.update(Y_)
                yield Y

        for Y in subsets_of(X):
            if Y.closure(F) not in R:
                return False
        return True

    def is_superkey(self, X: Attribute, F: Ft) -> bool:
        return X.closure(F) == self.to_attribute()

    def find_key(self, F: Ft) -> Attribute:
        return self.to_attribute().minimize(F)

    def find_3NF_decomposition(self, F: Ft) -> list["Relation"]:
        from .FunctionDependency import FunctionalDependencyGroup
        res = []
        # 1
        G = F.minimal_cover()

        # 2
        for f in G:
            X, A = f.tuple()
            res.append(X+A)

        # 3
        for decomp in res:
            if self.is_key(decomp, F):
                break
        else:
            res.append(self.find_key(F))

        # 4

        return [Relation.from_string(attr.symbol) for attr in res]

    def find_BCND_decomposition(self, F: Ft) -> list["Relation"]:
        pass

    @classmethod
    def from_string(self, s: str) -> "Relation":
        return Relation.from_strings(s.split())


__all__ = [
    "Relation"
]
