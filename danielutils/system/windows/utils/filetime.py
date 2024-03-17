from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FileTime:
    creation: Optional[datetime] = None
    modification: Optional[datetime] = None
    access: Optional[datetime] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\n\tcreation={str(self.creation)},\n\tmodification={str(self.modification)},\n\taceess={str(self.access)}\n)"


__all__ = [
    'FileTime'
]
