from typing import Iterable, get_args, Union, Set as Set
from ..reflection import get_python_version
if get_python_version() >= (3, 9):
    from builtins import set as Set


def to_set(x: Union[type, Iterable[type]]) -> Set[int]:
    """converts type/types to a set representing them
    """
    res: Set[int] = set()
    if hasattr(x, "__origin__") and x.__origin__ is Union:
        for xi in get_args(x):
            res.update(to_set(xi))
    elif isinstance(x, Iterable):
        for v in x:
            res.update(to_set(v))
        return res
    else:
        res.update(set([id(x)]))
    return res


def types_subseteq(a: Union[type, Iterable[type]], b: Union[type, Iterable[type]]) -> bool:
    """checks if 'a' is contained in 'b' typing wise

    Args:
        a (type | Iterable[type])
        b (type | Iterable[type])

    Returns:
        bool: result of containment
    """
    return to_set(a).issubset(to_set(b))


__all__ = [
    "types_subseteq"
]
