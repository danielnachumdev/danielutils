# -*- coding: utf-8 -*-
from .Decorators import validate
from .Functions import check_foreach

HEBREW_LETTERS = ['\u05D0', '\u2135', '\uFB21', '\uFB2E', '\uFB2F', '\uFB30', '\uFB4F', '\u05D1', '\u2136', '\uFB31', '\uFB4C', '\u05D2', '\u2137', '\uFB32', '\u05D3', '\u2138', '\uFB22', '\uFB33', '\u05D4', '\uFB23', '\uFB34', '\u05D5', '\uFB4B', '\uFB35', '\u05F0', '\u05F1', '\u05D6', '\uFB36', '\u05D7', '\u05D8', '\uFB38', '\u05D9', '\uFB1D', '\uFB39', '\u05EF', '\u05F2', '\uFB1F', '\u05DB', '\uFB24',
                  '\u05DA', '\uFB3B', '\uFB3A', '\uFB4D', '\u05DC', '\uFB25', '\uFB3C', '\u05DE', '\uFB26', '\u05DD', '\uFB3E', '\u05E0', '\u05DF', '\uFB40', '\u05E1', '\uFB41', '\u05E2', '\uFB20', '\u05E4', '\u05E3', '\uFB44', '\uFB43', '\uFB4E', '\u05E6', '\u05E5', '\uFB46', '\u05E7', '\uFB47', '\u05E8', '\uFB27', '\uFB48', '\u05E9', '\uFB2B', '\uFB2A', '\uFB49', '\uFB2D', '\uFB2C', '\u05EA', '\uFB28', '\uFB4A']
HEBREW_LETTERS_DEC = [ord(v) for v in HEBREW_LETTERS]
HEBREW_LETTERS_HEX = [hex(v) for v in HEBREW_LETTERS_DEC]
ENGLISH_LETTERS = [chr(v) for v in range(65, 91)]+[chr(v)
                                                   for v in range(97, 123)]
ENGLISH_LETTERS_DEC = [ord(v) for v in ENGLISH_LETTERS]
ENGLISH_LETTERS_HEX = [hex(v) for v in ENGLISH_LETTERS_DEC]


@validate(str, ret=bool)
def is_english(s: str) -> bool:
    return check_foreach(s, lambda c: c in ENGLISH_LETTERS)
    # try:
    #     s.encode(encoding='utf-8').decode('ascii')
    # except UnicodeDecodeError:
    #     return False
    # else:
    #     return True


@validate(str, ret=bool)
def is_int(text: str) -> bool:
    return text.isnumeric()


@validate(str, ret=bool)
def is_float(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False


@validate(str, ret=bool)
def is_number(text: str) -> bool:
    return is_float(text)


@validate(str, ret=bool)
def is_hebrew(text: str) -> bool:
    return check_foreach(text, lambda c: c in HEBREW_LETTERS)


@validate(str, ret=bool)
def is_binary(text: str) -> bool:
    return check_foreach(text, lambda c: c in [0, 1])


@validate(str, ret=bool)
def is_decimal(text: str) -> bool:
    return check_foreach(text, lambda c: c in range(10))


@validate(str, ret=bool)
def is_hex(h: str) -> bool:
    try:
        int(h, 16)
        return True
    except ValueError:
        return False


# __all__ = [
#     HEBREW_LETTERS,
#     HEBREW_LETTERS_DEC,
#     HEBREW_LETTERS_HEX,
#     ENGLISH_LETTERS,
#     ENGLISH_LETTERS_DEC,
#     ENGLISH_LETTERS_DEC,
#     ENGLISH_LETTERS_HEX,
# ]
