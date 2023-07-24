import types
from typing import Iterable, get_args, Union


def types_subseteq(a: Union[type, Iterable[type]], b: Union[type, Iterable[type]]) -> bool:
    """checks if 'a' is contained in 'b' typing wise

    Args:
        a (type | Iterable[type])
        b (type | Iterable[type])

    Returns:
        bool: result of containment
    """
    def to_set(x) -> set[int]:
        res: set[int] = set()
        if type(x) in {types.UnionType}:
            for xi in get_args(x):
                res.update(to_set(xi))
        elif isinstance(x, Iterable):
            for v in x:
                res.update(to_set(v))
            return res
        else:
            res.update(set([id(x)]))
        return res

    return to_set(a).issubset(to_set(b))


__all__ = [
    "types_subseteq"
]
