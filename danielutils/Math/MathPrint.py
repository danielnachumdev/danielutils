import sys
from ..Functions import areoneof
from .MathSymbols import subscript_dict, superscript_dict


def __mprint_parse_one(s: str) -> str:

    def inner(res, index, dct):
        start = index
        while index < len(s) and s[index] not in {' ', '*', '+', '-', '/', '_', '^'}:
            index += 1
        end = index
        for c in s[start:end]:
            if c in dct:
                res += dct[c]
            else:
                res += c
        index -= 1
        return res, index
    res: str = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c == "^":
            i += 1
            res, i = inner(res, i, superscript_dict)
        elif c == "_":
            i += 1
            res, i = inner(res, i, subscript_dict)
        else:
            res += c
        i += 1
    return res


def mprint(*args: list[str], sep=" ", end="\n", stream=sys.stdout) -> None:
    if not areoneof([*args], [str]):
        raise TypeError("s must be a string")
    stream.write(sep.join([__mprint_parse_one(s) for s in args])+end)


__all__ = [
    "mprint"
]
