import types
from typing import Iterable, get_args


def types_subseteq(a: type | Iterable[type], b: type | Iterable[type]) -> bool:
    """checks if 'a' is contained in 'b' typing wise

    Args:
        a (type | Iterable[type])
        b (type | Iterable[type])

    Returns:
        bool: result of containment
    """
    def to_set(x) -> set[int]:
        if type(x) in {types.UnionType}:
            return set(id(xi) for xi in get_args(x))

        return set([id(x)])

    return to_set(a).issubset(to_set(b))


__all__ = [
    "types_subseteq"
]
