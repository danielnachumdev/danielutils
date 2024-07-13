from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


@dataclass
class Field:
    """
    A Field object for a Section in a file

    Params:
        name (str): The name of the field
        size (int): The size of the field in bytes
        type (Field.Type): The type of the field
    """

    class Type(Enum):
        INTEGER = "INTEGER"
        FLOAT = "FLOAT"
        STRING = "STRING"
        BOOL = "BOOL"

    name: str
    size: int
    type: Type = Type.INTEGER


@dataclass
class Section:
    name: str
    prefix: bytes
    fields: Optional[List[Field]]
    is_optional: bool = False


class FileSpecification:
    def __init__(self, long_name: str, short_name: str, extension: str, specification: str,
                 sections: List[Section]) -> None:
        """

        Args:
            long_name:
            short_name:
            extension:
            specification:
            sections:
        """
        self.long_name = long_name
        self.short_name = short_name
        self.extension = extension
        self.specification = specification
        self.sections = sections

    def open(self, path: str):
        if not path.endswith(self.extension):
            raise ValueError(f"Invalid file extension, expected {self.extension}")
        with open(path, "rb") as f:
            lines = f.readlines()
        for line in lines:
            for b in line:
                pass

        return lines


__all__ = [
    "Field",
    "Section",
    "FileSpecification",
    "FileSpecification",
]
