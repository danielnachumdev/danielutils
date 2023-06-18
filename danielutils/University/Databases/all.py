from typing import Generator, Iterable, Optional
from ...Functions import powerset
from ...Generators import generate_except
from ...Decorators import PartiallyImplemented
from ...DataStructures import Queue


class Attribute:
    @classmethod
    def create_many(cls, amount: int, offset: int = 0) -> list["Attribute"]:
        res = []
        ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(offset, min(amount, len(ABC))):
            res.append(Attribute(ABC[i]))
        return res

    def __init__(self, symbol: Optional[str] = None):
        if symbol is None:
            symbol = ""
        self.symbol = "".join(sorted(symbol))

    def __len__(self) -> int:
        return len(self.symbol)

    def __add__(self, other: "Attribute") -> "Attribute":
        return self.union(other)

    def __sub__(self, other: "Attribute") -> "Attribute":
        return Attribute(self.symbol.replace(other.symbol, ""))

    def __lt__(self, other) -> int:
        return self.symbol < other.symbol

    def __contains__(self, other) -> bool:
        if isinstance(other, Attribute):
            return other.to_set().issubset(self.to_set())
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, Attribute):
            return self.symbol == other.symbol
        return False

    def __iter__(self) -> Generator["Attribute", None, None]:
        for v in self.symbol:
            yield Attribute(v)

    def __hash__(self) -> int:
        return hash(self.symbol)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return self.symbol

    def minimize(self, F: "FunctionalDependencyGroup") -> "Attribute":
        X = self.clone()
        for A in X:
            if A in (X-A).closure(F):
                X -= A
        return X

    def closure(self, F: Iterable["FunctionDependency"]) -> "Attribute":
        X = self

        # modified: algorithm from week 8
        V = X.clone()
        while True:
            V_ = V.clone()
            for dep in F:
                Y, Z = dep.X, dep.Y
                if Y in V:
                    if Z not in V:
                        V += Z
            if V == V_:
                break
        return V

    def update(self, other: "Attribute") -> "Attribute":
        self.symbol = str(''.join(
            sorted(str("".join(list(
                set(self.symbol).union(set(other.symbol))
            ))).upper())))
        return self

    def union(self, other: "Attribute") -> "Attribute":
        return Attribute(''.join(sorted(str("".join(list(set(self.symbol).union(set(other.symbol))))).upper())))

    def intersection(self, other: "Attribute") -> "Attribute":
        lst = list(
            set(str(self)).intersection(set(str(other)))
        )
        return Attribute(''.join(lst))

    def to_set(self) -> set["Attribute"]:
        return set([Attribute(v) for v in self.symbol])

    def clone(self) -> "Attribute":
        return Attribute("".join(self.symbol[:]))

    def is_empty(self) -> bool:
        return len(self) == 0


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

    def is_preserved_by(self, relations: list["Relation"], functional_dependencies: "FunctionalDependencyGroup"):
        # week 10 page 2 slide 3
        raise NotImplementedError()
        # for dep in functional_dependencies:
        #     if not dep.is_preserved_by(relations, functional_dependencies):
        #         return False
        # return True

    def __len__(self) -> int:
        return len(self.attributes)

    def subsets(self) -> Generator[Attribute, None, None]:
        for tup in generate_except(powerset(self), lambda index, _: index == 0):
            res = tup[0]
            for attr in tup[1:]:
                res = res.union(attr)
            yield res

    def is_BCNF(self, F: "FunctionalDependencyGroup") -> bool:
        for f in F:
            X, Y = f.tuple()
            if not (f.is_trivial() or self.is_superkey(X, F)):
                return False
        return True

    def is_3NF(self, F: "FunctionalDependencyGroup") -> bool:
        def second_condition(X: Attribute, Y: Attribute) -> bool:
            keys = self.find_all_keys(F)

            def is_in_any_key(A: Attribute) -> bool:
                for key in keys:
                    if A in key:
                        return True
                return False
            for A in Y:
                if not (A in X or is_in_any_key(A)):
                    return False
            return True
        for X, Y in F.tuples():
            if not (self.is_superkey(X, F) or second_condition(X, Y)):
                return False
        return True

    def is_key(self, X: Attribute, F: "FunctionalDependencyGroup") -> bool:
        if not self.is_superkey(X, F):
            return False
        R = self.to_attribute()

        def subsets_of(X: Attribute):
            for tup in generate_except(powerset(X), lambda _, v: len(v) in {0, len(X)}):
                Y = tup[0]
                for Y_ in tup[1:]:
                    Y.update(Y_)
                yield Y

        for Y in subsets_of(X):
            if Y.closure(F) not in R:
                return False
        return True

    def is_superkey(self, X: Attribute, F: "FunctionalDependencyGroup") -> bool:
        return X.closure(F) == self.to_attribute()

    def find_key(self, F: "FunctionalDependencyGroup") -> Attribute:
        return self.to_attribute().minimize(F)

    def find_all_keys(self, F: "FunctionalDependencyGroup") -> set[Attribute]:
        # week 9 slide 3
        K = self.find_key(F)
        KeyQueue = Queue()
        KeyQueue.push(K)
        Keys = set([K])
        while not KeyQueue.is_empty():
            K = KeyQueue.pop()
            for X, Y in F.tuples():
                if not Y.intersection(K).is_empty():
                    S = (K-Y).union(X)

                    for k in Keys:
                        if k in S:
                            break
                    else:
                        S_ = S.minimize(F)
                        KeyQueue.push(S_)
                        Keys.add(S_)
        return Keys

    def find_3NF_decomposition(self, F: "FunctionalDependencyGroup") -> list["Relation"]:
        # TODO add backtracking so this will be deterministic with the correct result
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
        # TODO
        return [Relation.from_string(attr.symbol) for attr in res]

    def find_BCND_decomposition(self, F: "FunctionalDependencyGroup") -> list["Relation"]:
        """week 10 page 16 slide 2
        """
        def get_violation() -> tuple[Attribute, Attribute]:
            for f in F:
                X, Y = f.tuple()
                if not (f.is_trivial() or self.is_superkey(X, F)):
                    break
            return X, Y

        if self.is_BCNF(F):
            return [self]

        X, Y = get_violation()
        closure = X.closure(F)
        R1 = Relation([A for A in closure])
        R2 = Relation([A for A in X.union(self.to_attribute()-closure)])

        F_R1 = F.project_on(R1)
        F_R2 = F.project_on(R2)
        return R1.find_BCND_decomposition(F_R1) + R2.find_BCND_decomposition(F_R2)

    @classmethod
    def from_string(self, s: str) -> "Relation":
        return Relation.from_strings(s.split())


class FunctionDependency:

    @classmethod
    def from_string(cls, s: str) -> "FunctionDependency":
        key, value = s.split("->")
        return cls(key, value)

    # def is_preserved_by(self, potential_decomposition: list[Relation], functional_dependencies: "FunctionalDependencyGroup") -> bool:
    #     for dependency in functional_dependencies:
    #         X, Y = dependency.X, dependency.Y
    #         Z = X.clone()
    #         predicate = True
    #         Z_ = Z.clone()
    #         while predicate:
    #             for R in (r.to_attribute() for r in potential_decomposition):
    #                 Z = Z.union(
    #                     Z.intersection(R)
    #                     .closure(functional_dependencies)
    #                     .intersection(R)
    #                 )

    #             if Z_ == Z:
    #                 predicate = False
    #         if Y not in Z:
    #             return False
    #     return True

    def is_trivial(self) -> bool:
        return self.Y in self.X

    @classmethod
    def from_attributes(cls, key: Attribute, value: Attribute) -> "FunctionDependency":
        return cls(key.symbol, value.symbol)

    def __init__(self, key: str | Attribute, value: str | Attribute):
        if isinstance(key, str):
            key = Attribute(key)
        if isinstance(value, str):
            value = Attribute(value)
        self.X: Attribute = key.clone()
        self.Y: Attribute = value.clone()

    def __eq__(self, other) -> bool:
        if isinstance(other, FunctionDependency):
            return self.X == other.X and self.Y == other.Y
        return False

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"{self.X}->{self.Y}"

    def tuple(self) -> tuple[Attribute, Attribute]:
        return self.X, self.Y

    def __hash__(self) -> int:
        return -hash(self.X) + hash(self.Y)

    def follows_from(self, s: set["FunctionDependency"]) -> bool:
        if self in s:
            s.remove(self)

        return self.Y in self.X.closure(s)

    def __lt__(self, other: "FunctionDependency") -> int:
        a = self.X < other.X
        if a != 0:
            return a
        return self.Y < other.Y


class FunctionalDependencyGroup:
    def project_on(self, R: Relation) -> "FunctionalDependencyGroup":
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, dct: dict[str, str]) -> "FunctionalDependencyGroup":
        return cls([FunctionDependency(k, v) for k, v in dct.items()])

    def __init__(self, dependencies: Iterable[FunctionDependency]):
        self.dct: dict[Attribute, Attribute] = {}
        for dep in dependencies:
            X, Y = dep.tuple()
            if X not in self.dct:
                self.dct[X] = Y
            self.dct[X] += Y

    def add(self, f: FunctionDependency) -> "FunctionalDependencyGroup":
        X, Y = f.tuple()
        self.dct[X] = Y
        return self

    @PartiallyImplemented
    def minimal_cover(self) -> list[FunctionDependency]:
        G: set[FunctionDependency] = set()
        for X, Y in self.tuples():
            for A in Y:
                G.add(FunctionDependency.from_attributes(X, A))
        G_ = set()
        for f in set(G):
            X, A = f.tuple()
            if len(X) > 1:
                for B in X:
                    if A in (X-B).closure(self):
                        X -= B
            G_.add(FunctionDependency.from_attributes(X, A))
        G = set(G_)
        del G_
        for f in set(G):
            X, A = f.tuple()
            if f.follows_from(set(G)):
                G.remove(f)

        return list(sorted(G))  # type:ignore

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
    "Attribute",
    "Relation",
    "FunctionDependency",
    "FunctionalDependencyGroup"
]
