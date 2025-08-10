import ast
from enum import Enum
from typing import List, Union, Optional


class ImportType(Enum):
    """Enumeration of import types."""
    GLOBAL_PACKAGE = "global_package"           # "import x"
    GLOBAL_FROM_PACKAGE = "global_from_package"  # "from x import y"
    LOCAL_PACKAGE = "local_package"             # "import .x" or "import ..x"
    # "from .x import y" or "from ..x import y"
    LOCAL_FROM_PACKAGE = "local_from_package"


class ImportInfo:
    """
    A class that encapsulates information about a single import statement.

    This class provides detailed information about imports including:
    - The type of import (global vs local, package vs from_package)
    - Whether the import is absolute or relative
    - Module names and imported object names
    - Aliases used in the import
    """

    def __init__(self,
                 import_type: ImportType,
                 is_absolute: bool,
                 module_name: str,
                 imported_object: Optional[str] = None,
                 alias: Optional[str] = None,
                 relative_level: int = 0) -> None:
        """
        Initialize ImportInfo.

        :param import_type: The type of import (from ImportType enum)
        :param is_absolute: Whether the import is absolute (True) or relative (False)
        :param module_name: The name of the module being imported from
        :param imported_object: The name of the specific object being imported (for from imports)
        :param alias: The alias used for the import (if any)
        :param relative_level: The number of dots for relative imports (0 for absolute)
        """
        self._import_type = import_type
        self._is_absolute = is_absolute
        self._module_name = module_name
        self._imported_object = imported_object
        self._alias = alias
        self._relative_level = relative_level

    @property
    def import_type(self) -> ImportType:
        """Returns the type of import."""
        return self._import_type

    @property
    def is_absolute(self) -> bool:
        """Returns True if the import is absolute, False if relative."""
        return self._is_absolute

    @property
    def is_relative(self) -> bool:
        """Returns True if the import is relative, False if absolute."""
        return not self._is_absolute

    @property
    def module_name(self) -> str:
        """Returns the name of the module being imported from."""
        return self._module_name

    @property
    def imported_object(self) -> Optional[str]:
        """Returns the name of the imported object (for from imports)."""
        return self._imported_object

    @property
    def alias(self) -> Optional[str]:
        """Returns the alias used for the import (if any)."""
        return self._alias

    @property
    def relative_level(self) -> int:
        """Returns the number of dots for relative imports (0 for absolute)."""
        return self._relative_level

    @property
    def effective_name(self) -> str:
        """Returns the effective name used in the code (alias if provided, otherwise imported_object or module_name)."""
        if self.alias:
            return self.alias
        elif self.imported_object:
            return self.imported_object
        else:
            return self.module_name.split('.')[-1]

    def __str__(self) -> str:
        return (f"ImportInfo(type={self.import_type.value}, "
                f"absolute={self.is_absolute}, "
                f"module='{self.module_name}', "
                f"object={self.imported_object}, "
                f"alias={self.alias})")

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the import information."""
        return {
            "import_type": self.import_type.value,
            "is_absolute": self.is_absolute,
            "module_name": self.module_name,
            "imported_object": self.imported_object,
            "alias": self.alias,
            "relative_level": self.relative_level,
            "effective_name": self.effective_name
        }

    @classmethod
    def from_ast(cls, node: Union[ast.Import, ast.ImportFrom]) -> List["ImportInfo"]:
        """
        Create ImportInfo instances from AST nodes.

        :param node: An ast.Import or ast.ImportFrom node
        :return: A list of ImportInfo objects
        """
        imports = []

        if isinstance(node, ast.Import):
            # Handle "import x" statements
            for alias in node.names:
                module_name = alias.name
                is_absolute = not module_name.startswith('.')
                relative_level = 0

                if not is_absolute:
                    # Count leading dots for relative imports
                    relative_level = len(module_name) - \
                        len(module_name.lstrip('.'))
                    module_name = module_name[relative_level:]

                import_type = ImportType.LOCAL_PACKAGE if not is_absolute else ImportType.GLOBAL_PACKAGE

                imports.append(cls(
                    import_type=import_type,
                    is_absolute=is_absolute,
                    module_name=module_name,
                    imported_object=None,
                    alias=alias.asname,
                    relative_level=relative_level
                ))

        elif isinstance(node, ast.ImportFrom):
            # Handle "from x import y" statements
            module_name = node.module if node.module is not None else ""
            is_absolute = True  # Default to absolute
            relative_level = 0

            # Check if this is a relative import by looking at the level attribute
            if hasattr(node, 'level') and node.level > 0:
                is_absolute = False
                relative_level = node.level
            elif module_name.startswith('.'):
                # Fallback: check if module name starts with dots
                is_absolute = False
                relative_level = len(module_name) - \
                    len(module_name.lstrip('.'))
                module_name = module_name[relative_level:]

            import_type = ImportType.LOCAL_FROM_PACKAGE if not is_absolute else ImportType.GLOBAL_FROM_PACKAGE

            for alias in node.names:
                imported_object = alias.name
                imports.append(cls(
                    import_type=import_type,
                    is_absolute=is_absolute,
                    module_name=module_name,
                    imported_object=imported_object,
                    alias=alias.asname,
                    relative_level=relative_level
                ))

        return imports

    @classmethod
    def from_string(cls, import_string: str) -> List["ImportInfo"]:
        """
        Create ImportInfo instances from a string representation of import statements.

        :param import_string: A string containing import statements
        :return: A list of ImportInfo objects
        """
        try:
            tree = ast.parse(import_string)
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.extend(cls.from_ast(node))

            return imports
        except SyntaxError:
            raise ValueError(f"Invalid import string: {import_string}")


__all__ = [
    "ImportInfo",
    "ImportType"
]
