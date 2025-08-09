import ast
import tokenize
import io
import importlib.util
import inspect
from collections import Counter
from pathlib import Path
from typing import List, Set, Dict, Any

from .import_info import ImportInfo
from .class_info import ClassInfo
from .function_info import FunctionInfo


class FileInfo:
    """
    A class for static analysis of a Python source file.

    Analysis includes:
      • Tokenization: token count and token frequency distribution.
      • Extraction of comments.
      • Listing names of classes and functions.
      • Identification of import statements, now represented by ImportInfo objects.
      • Basic import usage analysis (which imports appear to be used).
      • (Dynamic) loading of the file to create detailed ClassInfo and FunctionInfo objects.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = str(Path(file_path).resolve())
        self._content: str = self._read_file()
        self._tree: ast.AST = self._parse_content()
        self._tokens: List[tokenize.TokenInfo] = None

    def _read_file(self) -> str:
        """Reads and returns the file content as UTF-8 text."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading {self.file_path}: {e}")

    def _parse_content(self) -> ast.AST:
        """Parses the file content into an AST."""
        try:
            return ast.parse(self._content, filename=self.file_path)
        except Exception as e:
            raise Exception(f"Error parsing {self.file_path}: {e}")

    def _tokenize(self) -> None:
        """Tokenizes the file content using tokenize.tokenize()."""
        self._tokens = []
        stream = io.BytesIO(self._content.encode("utf-8"))
        try:
            for tok in tokenize.tokenize(stream.readline):
                if tok.type == tokenize.ENCODING:
                    continue
                self._tokens.append(tok)
        except tokenize.TokenError as te:
            print(f"Tokenize error: {te}")

    @property
    def tokens(self) -> List[tokenize.TokenInfo]:
        """Returns the list of tokens from the file."""
        if self._tokens is None:
            self._tokenize()
        return self._tokens

    @property
    def token_count(self) -> int:
        """Total number of tokens in the file."""
        return len(self.tokens)

    @property
    def token_distribution(self) -> Dict[str, int]:
        """A dictionary mapping token strings to their frequency."""
        return dict(Counter(tok.string for tok in self.tokens))

    @property
    def comments(self) -> List[str]:
        """A list of all comment strings in the file."""
        return [tok.string for tok in self.tokens if tok.type == tokenize.COMMENT]

    @property
    def class_names(self) -> List[str]:
        """Names of all classes defined in the file."""
        return [node.name for node in ast.walk(self._tree) if isinstance(node, ast.ClassDef)]

    @property
    def function_names(self) -> List[str]:
        """Names of all functions (including async) defined in the file."""
        return [
            node.name
            for node in ast.walk(self._tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

    @property
    def imports(self) -> List[Any]:
        """
        Returns a list of ImportInfo objects representing all import statements.
        Each AST node of type ast.Import or ast.ImportFrom is transformed via
        ImportInfo.from_ast().
        """
        results = []
        if ImportInfo is None:
            return results
        for node in ast.walk(self._tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                results.extend(ImportInfo.from_ast(node))
        return results

    @property
    def used_names(self) -> Set[str]:
        """
        A set of all names (identifiers) used in the file,
        based on ast.Name nodes.
        """
        names = set()
        for node in ast.walk(self._tree):
            if isinstance(node, ast.Name):
                names.add(node.id)
        return names

    @property
    def import_usage(self) -> Dict[str, List[Any]]:
        """
        Returns a dictionary with two keys:
          • 'used' : list of ImportInfo objects for which the alias is found in the file,
          • 'unused' : list of ImportInfo objects whose alias is never referenced.
        Wildcard imports (alias "*") are assumed to be used.
        """
        used, unused = [], []
        for imp in self.imports:
            if imp.alias == "*" or imp.alias is None or imp.alias in self.used_names:
                used.append(imp)
            else:
                unused.append(imp)
        return {"used": used, "unused": unused}

    def _load_module(self) -> Any:
        """
        Dynamically loads the file as a module and returns the module object.
        Returns None if the loading fails.

        Warning: This executes the file's top-level code.
        """
        try:
            module_name = "_temp_module_" + str(abs(hash(self.file_path)))
            spec = importlib.util.spec_from_file_location(module_name, self.file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"Error loading module from {self.file_path}: {e}")
            return None

    def get_dynamic_class_info(self) -> List[Any]:
        """
        Dynamically imports the file as a module and returns a list of ClassInfo objects,
        one per class defined at module level.

        Warning: This executes the file's top-level code.
        """
        if ClassInfo is None:
            print("ClassInfo unavailable; skipping dynamic class analysis.")
            return []
        module = self._load_module()
        if module is None:
            return []
        infos = []
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if inspect.getmodule(obj) == module:
                try:
                    infos.append(ClassInfo(obj))
                except Exception as e:
                    print(f"Error processing class {name}: {e}")
        return infos

    def get_dynamic_function_info(self) -> List[Any]:
        """
        Dynamically imports the file as a module and returns a list of FunctionInfo objects,
        one per function defined at module level.

        Warning: This executes the file's top-level code.
        """
        if FunctionInfo is None:
            print("FunctionInfo unavailable; skipping dynamic function analysis.")
            return []
        module = self._load_module()
        if module is None:
            return []
        infos = []
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if inspect.getmodule(obj) == module:
                try:
                    infos.append(FunctionInfo(obj))
                except Exception as e:
                    print(f"Error processing function {name}: {e}")
        return infos

    def print_summary(self) -> None:
        """Prints a detailed summary of all analyses of the file."""
        print(f"===== Analysis of {self.file_path} =====")

        print(f"\nToken Count: {self.token_count}")
        print("\nToken Distribution (Top 10):")
        for token, count in sorted(self.token_distribution.items(), key=lambda x: -x[1])[:10]:
            print(f"  {repr(token)}: {count}")

        print("\nComments Found:")
        if self.comments:
            for comment in self.comments:
                print(" ", comment)
        else:
            print("  (None)")

        print("\nClasses Defined:")
        if self.class_names:
            for cls in self.class_names:
                print(" ", cls)
        else:
            print("  (None)")

        print("\nFunctions Defined:")
        if self.function_names:
            for fn in self.function_names:
                print(" ", fn)
        else:
            print("  (None)")

        print("\nImports Found:")
        for imp in self.imports:
            print(f"  {imp.alias} from {imp.module} ({imp.kind})")

        usage = self.import_usage
        print("\nUsed Imports:")
        for imp in usage["used"]:
            print(f"  {imp.alias} from {imp.module} ({imp.kind})")

        print("\nUnused Imports:")
        if usage["unused"]:
            for imp in usage["unused"]:
                print(f"  {imp.alias} from {imp.module} ({imp.kind})")
        else:
            print("  (None)")

        print("\nDetailed Class Info:")
        dynamic_class_infos = self.get_dynamic_class_info()
        if dynamic_class_infos:
            for info in dynamic_class_infos:
                print(info)
        else:
            print("  (None)")

        print("\nDetailed Function Info:")
        dynamic_function_infos = self.get_dynamic_function_info()
        if dynamic_function_infos:
            for info in dynamic_function_infos:
                print(info)
        else:
            print("  (None)")
        print("========================================")


__all__ = [
    "FileInfo"
]
