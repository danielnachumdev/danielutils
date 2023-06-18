from typing import Generator, ForwardRef, Iterable

F_t = ForwardRef("FunctionalDependencyGroup")


class Attribute:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def __len__(self) -> int:
        return len(self.symbol)

    def __add__(self, other: "Attribute") -> "Attribute":
        return self.union(other)

    def __sub__(self, other: "Attribute") -> "Attribute":
        return Attribute(self.symbol.replace(other.symbol, ""))

    def minimize(self, F: F_t) -> "Attribute":
        X = self.clone()
        for A in X:
            if A in (X-A).closure(F):
                X -= A
        return X

    def closure(self, F: Iterable["FunctionalDependency"]) -> "Attribute":
        X = self

        # modified: algorithm from week 8
        V = X.clone()
        while True:
            V_ = V.clone()
            for dep in F:
                Y, Z = dep.key, dep.value
                if Y in V:
                    if Z not in V:
                        V += Z
            if V == V_:
                break
        return V

    def __lt__(self, other) -> int:
        return self.symbol < other.symbol

    def update(self, other: "Attribute") -> "Attribute":
        self.symbol = str(''.join(
            sorted(str("".join(list(
                set(self.symbol).union(set(other.symbol))
            ))).upper())))
        return self

    def __contains__(self, other) -> bool:
        if isinstance(other, Attribute):
            return other.to_set().issubset(self.to_set())
        return False

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
        return Attribute(self.symbol)

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


__all__ = [
    "Attribute"
]
