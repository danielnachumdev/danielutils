from abc import ABC, abstractmethod
from typing import Protocol


class LanguageItem(Protocol): ...


class Language(ABC):

    @abstractmethod
    def __contains__(self, item: LanguageItem) -> bool: ...


__all__ = [
    "Language",
    "LanguageItem"
]
