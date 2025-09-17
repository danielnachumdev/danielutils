# -*- coding: utf-8 -*-
import logging
from typing import Union
from .decorators.validate import validate
from .functions.check_foreach import check_foreach
from .logging_.utils import get_logger

logger = get_logger(__name__)
HEBREW_LETTERS = ['\u05D0', '\u2135', '\uFB21', '\uFB2E', '\uFB2F',
                  '\uFB30', '\uFB4F', '\u05D1', '\u2136', '\uFB31',
                  '\uFB4C', '\u05D2', '\u2137', '\uFB32', '\u05D3',
                  '\u2138', '\uFB22', '\uFB33', '\u05D4', '\uFB23',
                  '\uFB34', '\u05D5', '\uFB4B', '\uFB35', '\u05F0',
                  '\u05F1', '\u05D6', '\uFB36', '\u05D7', '\u05D8',
                  '\uFB38', '\u05D9', '\uFB1D', '\uFB39', '\u05EF',
                  '\u05F2', '\uFB1F', '\u05DB', '\uFB24', '\u05DA',
                  '\uFB3B', '\uFB3A', '\uFB4D', '\u05DC', '\uFB25',
                  '\uFB3C', '\u05DE', '\uFB26', '\u05DD', '\uFB3E',
                  '\u05E0', '\u05DF', '\uFB40', '\u05E1', '\uFB41',
                  '\u05E2', '\uFB20', '\u05E4', '\u05E3', '\uFB44',
                  '\uFB43', '\uFB4E', '\u05E6', '\u05E5', '\uFB46',
                  '\u05E7', '\uFB47', '\u05E8', '\uFB27', '\uFB48',
                  '\u05E9', '\uFB2B', '\uFB2A', '\uFB49', '\uFB2D',
                  '\uFB2C', '\u05EA', '\uFB28', '\uFB4A']


HEBREW_LETTERS_DEC = [ord(v) for v in HEBREW_LETTERS]
HEBREW_LETTERS_HEX = [hex(v) for v in HEBREW_LETTERS_DEC]
ENGLISH_LETTERS = [chr(v) for v in range(65, 91)]+[chr(v)
                                                   for v in range(97, 123)]
ENGLISH_LETTERS_DEC = [ord(v) for v in ENGLISH_LETTERS]
ENGLISH_LETTERS_HEX = [hex(v) for v in ENGLISH_LETTERS_DEC]


@validate  # type:ignore
def is_english(s: str) -> bool:
    """returns whether the specified string is in the english language

    Args:
        s (str): the string to check

    Returns:
        bool: returns true if the string is in english
    """
    return check_foreach(s, lambda c: c in ENGLISH_LETTERS)


@validate  # type:ignore
def is_number(s: str) -> bool:
    """checks if a string is a number

    Args:
        text (str): string to check

    Returns:
        bool: true if string is a number
    """
    return s.isnumeric()


@validate  # type:ignore
def is_int(num: Union[int, float]) -> bool:
    """_summary_

    Args:
        num (Union[int, float]): is a number an int

    Returns:
        bool: return true if num is a while number
    """
    if isinstance(num, int):
        return True

    return int(num) == num


@validate  # type:ignore
def is_float(s: str) -> bool:
    """checks whether a string has a float value

    Args:
        s (str): string to check

    Returns:
        bool: result
    """
    try:
        float(s)
        logger.debug(f"String '{s}' is a valid float")
        return True
    except ValueError:
        logger.debug(f"String '{s}' is not a valid float")
        return False


@validate  # type:ignore
def is_hebrew(s: str) -> bool:
    """checks if a string is in hebrew

    Args:
        text (str): string to check

    Returns:
        bool: true iff all chars are hebrew
    """
    return check_foreach(s, lambda c: c in HEBREW_LETTERS)


@validate  # type:ignore
def is_binary(s: str) -> bool:
    """checks if s string has a binary value

    Args:
        s (str): string to check

    Returns:
        bool: result
    """
    return check_foreach(s, lambda c: c in {0, 1})


@validate  # type:ignore
def is_decimal(s: str) -> bool:
    """checks if a string has a decimal number

    Args:
        s (str): string to check

    Returns:
        bool: result
    """
    return check_foreach(s, lambda c: c in range(10))


@validate  # type:ignore
def is_hex(s: str) -> bool:
    """checks if a string has a hexadecimal value

    Args:
        s (str): string to check

    Returns:
        bool: result
    """
    try:
        int(s, 16)
        logger.debug(f"String '{s}' is a valid hexadecimal")
        return True
    except ValueError:
        logger.debug(f"String '{s}' is not a valid hexadecimal")
        return False


__all__ = [
    "HEBREW_LETTERS",
    "HEBREW_LETTERS_DEC",
    "HEBREW_LETTERS_HEX",
    "ENGLISH_LETTERS",
    "ENGLISH_LETTERS_DEC",
    "ENGLISH_LETTERS_HEX",
    "is_english",
    "is_number",
    "is_int",
    "is_float",
    "is_hebrew",
    "is_binary",
    "is_decimal",
    "is_hex"
]
