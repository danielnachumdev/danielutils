import ast
from typing import List, Union


class ImportInfo:
    """
    A class that encapsulates information about a single import statement element.

    Depending on how the import appears in the source code, this may represent:
      - a regular import (e.g., "import os" or "import os.path as osp"),
      - a from-import (e.g., "from sys import version_info"), or
      - a wildcard import (e.g., "from math import *").

    The exposed properties are:
      • alias: The accessible name in the file.
      • module: The imported module or package.
      • kind: A short string indicating the type. It will be one of:
          "import", "from_import", or "from_import_all".
    """

    def __init__(self, alias: str, module: str, kind: str) -> None:
        """
        :param alias: The name used in the current file. For example, in
                      "import os as myos", the alias is 'myos'; if no alias is given,
                      a default is provided (e.g., the top-level module name).
        :param module: The full module or package name (e.g., "os", or "os.path").
        :param kind: A descriptor of the import kind: "import", "from_import", or "from_import_all".
        """
        self._alias = alias
        self._module = module
        self._kind = kind

    @property
    def alias(self) -> str:
        """Returns the alias (or name) used for the import in the file."""
        return self._alias

    @property
    def module(self) -> str:
        """Returns the module or package name as imported."""
        return self._module

    @property
    def kind(self) -> str:
        """
        Returns the type of import:
          - "import" for a standard import statement,
          - "from_import" for a 'from X import Y' statement,
          - "from_import_all" for a wildcard import (e.g., 'from X import *').
        """
        return self._kind

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the import information."""
        return {"alias": self.alias, "module": self.module, "kind": self.kind}

    def __str__(self) -> str:
        return f"ImportInfo(alias={self.alias!r}, module={self.module!r}, kind={self.kind!r})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_ast(cls, node: Union[ast.Import, ast.ImportFrom]) -> List["ImportInfo"]:
        """
        Given an AST node of type ast.Import or ast.ImportFrom, returns a list
        of ImportInfo instances representing each imported alias in that node.

        For an ast.Import node:
          • Each alias in node.names is processed.
          • If an alias is not provided (using the as keyword), then the first
            part of the module name (split by '.') is used as the alias.

        For an ast.ImportFrom node:
          • The module attribute (which can be None for relative imports) is used.
          • Each alias is processed. If alias.name equals "*", the import is considered a wildcard.

        :param node: An ast.Import or ast.ImportFrom node.
        :return: A list of ImportInfo objects.
        """
        imports = []
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Use asname if available; otherwise use the top-level name.
                local_alias = alias.asname if alias.asname else alias.name.split(".")[0]
                imports.append(cls(local_alias, alias.name, "import"))
        elif isinstance(node, ast.ImportFrom):
            modname = node.module if node.module is not None else ""
            for alias in node.names:
                if alias.name == "*":
                    imports.append(cls("*", modname, "from_import_all"))
                else:
                    local_alias = alias.asname if alias.asname else alias.name
                    imports.append(cls(local_alias, modname, "from_import"))
        return imports


__all__ = [
    "ImportInfo"
]
