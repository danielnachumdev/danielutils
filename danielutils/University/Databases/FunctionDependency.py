from typing import Generator, Iterable
from .Attribute import Attribute
from .Relation import Relation
from danielutils import PartiallyImplemented


class FunctionDependency:
    @classmethod
    def from_string(cls, s: str) -> "FunctionDependency":
        key, value = s.split("->")
        return cls(key, value)

    def is_preserved_by(self, potential_decomposition: list[Relation], functional_dependencies: "FunctionalDependencyGroup") -> bool:
        for dependency in functional_dependencies:
            X, Y = dependency.key, dependency.value
            Z = X.clone()
            predicate = True
            Z_ = Z.clone()
            while predicate:
                for R in (r.to_attribute() for r in potential_decomposition):
                    Z = Z.union(
                        Z.intersection(R)
                        .closure(functional_dependencies)
                        .intersection(R)
                    )

                if Z_ == Z:
                    predicate = False
            if Y not in Z:
                return False
        return True

    def is_trivial(self) -> bool:
        return self.value in self.key

    @classmethod
    def from_attributes(cls, key: Attribute, value: Attribute) -> "FunctionDependency":
        return cls(key.symbol, value.symbol)

    def __init__(self, key: str, value: str):
        self.key: Attribute = Attribute(key)
        self.value: Attribute = Attribute(value)

    def __eq__(self, other) -> bool:
        if isinstance(other, FunctionDependency):
            return self.key == other.key and self.value == other.value
        return False

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"{self.key}->{self.value}"

    def tuple(self) -> tuple[Attribute, Attribute]:
        return self.key, self.value

    def __hash__(self) -> int:
        return -hash(self.key) + hash(self.value)

    def follows_from(self, s: set["FunctionDependency"]) -> bool:
        if self in s:
            s.remove(self)

        return self.value in self.key.closure(s)

    def __lt__(self, other) -> int:
        a = self.key < other.key
        if a != 0:
            return a
        return self.value < other.value


class FunctionalDependencyGroup:
    @classmethod
    def from_dict(cls, dct: dict[str, str]) -> "FunctionalDependencyGroup":
        return cls([FunctionDependency(k, v) for k, v in dct.items()])

    def __init__(self, dependencies: Iterable[FunctionDependency]):
        self.dct: dict[Attribute, Attribute] = {
            dependency.key: dependency.value for dependency in dependencies}

    def add(self, f: FunctionDependency) -> "FunctionalDependencyGroup":
        X, Y = f.tuple()
        self.dct[X] = Y
        return self

    @PartiallyImplemented
    def minimal_cover(self) -> "FunctionalDependencyGroup":
        G = set()
        for X, Y in self.tuples():
            for A in Y:
                G.add(FunctionDependency.from_attributes(X, A))

        G_ = set()
        for f in G:
            X, A = f.tuple()
            if len(X) > 1:
                for B in X:
                    if A in (X-B).closure(self):
                        X -= B
            G_.add(FunctionDependency.from_attributes(X, A))
        G = G_

        G_ = set(G)
        for f in G:
            X, A = f.tuple()
            if f.follows_from(set(G_)):
                G_.remove(f)
        G = G_
        return list(sorted(G))

    def tuples(self) -> Generator[tuple[Attribute, Attribute], None, None]:
        for dep in self:
            yield dep.tuple()
    # def minimize(self) -> set[Attribute]::
    #     # q: Queue = Queue()
    #     # q.push_many(list(self.to_set()))
    #     # for _ in range(len(q)):
    #     #     excluded = q.pop()
    #     #     closure = set()
    #     #     for v in q:
    #     #         closure.update(v.closure(self))
    #     #     if closure != self.to_set():
    #     #         q.push(excluded)
    #     # return set(iter(q))

    def to_set(self) -> set[Attribute]:
        return set(self.dct.keys()).union(set(self.dct.values()))

    def __iter__(self) -> Generator[FunctionDependency, None, None]:
        for k, v in self.dct.items():
            yield FunctionDependency.from_attributes(k, v)

    def __str__(self) -> str:
        return repr(self)

    def __contains__(self, key: Attribute) -> bool:
        return key in self.dct

    def __getitem__(self, key: Attribute) -> Attribute:
        return self.dct[key]

    def __repr__(self) -> str:
        res = "{ "
        res += ", ".join(f"{k}->{v}" for k, v in self.dct.items())
        res += " }"
        return res


__all__ = [
    "FunctionDependency",
    "FunctionalDependencyGroup"
]
