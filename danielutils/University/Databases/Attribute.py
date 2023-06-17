from typing import Generator, ForwardRef
# from ..Databases import FunctionalDependencyGroup
ForwardRef("FunctionalDependencyGroup")


class Attribute:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def closure(self, relations: ForwardRef("FunctionalDependencyGroup")) -> "Attribute":
        queue: list[Attribute] = [self]
        res = self.clone()
        while len(queue) > 0:
            item = queue.pop()
            if item in relations:
                res = res.union(item)
                value = relations[item]
                if value not in res:
                    queue.append(value)
                for v in res:
                    candidate = value.union(v)
                    if candidate not in res:
                        queue.append(candidate)
                res = res.union(item)
        return res

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
