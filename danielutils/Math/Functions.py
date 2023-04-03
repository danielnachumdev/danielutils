from ..Typing import Union
from ..Decorators import validate_explicit


@validate_explicit([int, float])
def sign(v: Union[int, float]) -> int:
    if v == 0:
        return 1
    return abs(v)/v


__all__ = [
    "sign"
]
