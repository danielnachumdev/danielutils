from .MathSymbols import subscript_dict, superscript_dict


def mprint_parse_one(s: str) -> str:
    """a helper function that parses "mathematically" one string

    Args:
        s (str): the string to parse with math symbols

    Returns:
        str: the result
    """

    def inner(res: str, index: int, dct: dict):
        start = index
        while index < len(s) and s[index] not in {' ', '*', '+', '-', '/', '_', '^'}:
            index += 1
        end = index
        for char in s[start:end]:
            if char in dct:
                res += dct[char]
            else:
                res += char
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


__all__ = [
    "mprint_parse_one"
]
