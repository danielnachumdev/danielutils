import random

LOWERCASE_LETTERS: str = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE_LETTERS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS = LOWERCASE_LETTERS + UPPERCASE_LETTERS
DIGITS: str = "0123456789"
ALL = LETTERS + DIGITS


def builder(length: int, letters: str) -> str:
    return "".join(random.choices(letters, k=length))


class RandomDataGenerator:

    @staticmethod
    def string(length: int) -> str:
        return builder(length, ALL)

    @staticmethod
    def name(length: int) -> str:
        return builder(length, LETTERS)

    @staticmethod
    def file_name(length: int) -> str:
        return "file_" + RandomDataGenerator.name(length)

    @staticmethod
    def directory_name(length: int) -> str:
        return "directory_" + RandomDataGenerator.name(length)

    @staticmethod
    def number(minimum: int, exclusive_maximum: int) -> int:
        return random.randint(minimum, exclusive_maximum)

    @staticmethod
    def integer(minimum: int, exclusive_maximum: int) -> int:
        return random.randint(minimum, exclusive_maximum)

    @staticmethod
    def float(minimum: float, exclusive_maximum: float) -> float:
        return random.uniform(minimum, exclusive_maximum)


__all__ = [
    "RandomDataGenerator",
]
