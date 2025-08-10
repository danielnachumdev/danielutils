import ast
import tokenize
import io
import importlib.util
import inspect
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Set, Dict, Any, Optional, Tuple
from enum import Enum

from .import_info import ImportInfo, ImportType
from .class_info import ClassInfo
from .function_info import FunctionInfo


class CodeQualityLevel(Enum):
    """Enumeration of code quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNKNOWN = "unknown"


class FileInfo:
    """
    A comprehensive class for static and dynamic analysis of Python source files.

    Analysis includes:
      • Tokenization: token count, frequency distribution, and analysis
      • Code metrics: line counts, complexity, size analysis
      • Structure analysis: classes, functions, imports, and their relationships
      • Import analysis: detailed import categorization and dependency tracking
      • Code quality: style analysis, documentation coverage, type hints
      • Dynamic analysis: runtime inspection of loaded modules
      • Export capabilities: JSON, summary reports, and data structures
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize FileInfo with a file path.

        :param file_path: Path to the Python source file to analyze
        """
        self.file_path = str(Path(file_path).resolve())
        self._content: str = self._read_file()
        self._tree: ast.AST = self._parse_content()
        self._tokens: List[tokenize.TokenInfo] = None
        self._lines: List[str] = None
        self._imports: List[ImportInfo] = None
        self._import_stats: Dict[str, Any] = None
        self._code_metrics: Dict[str, Any] = None
        self._structure_info: Dict[str, Any] = None

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

    def _parse_lines(self) -> None:
        """Parse the file content into lines for analysis."""
        self._lines = self._content.splitlines()
        # Handle empty file case
        if not self._lines and not self._content.strip():
            self._lines = []

    def _analyze_imports(self) -> None:
        """Analyze imports and create comprehensive import statistics."""
        if self._imports is not None:
            return

        self._imports = []
        for node in ast.walk(self._tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self._imports.extend(ImportInfo.from_ast(node))

        # Calculate import statistics
        self._import_stats = {
            'total_imports': len(self._imports),
            'by_type': defaultdict(int),
            'by_scope': {'absolute': 0, 'relative': 0},
            'modules': set(),
            'unused_count': 0,
            'used_count': 0
        }

        for imp in self._imports:
            self._import_stats['by_type'][imp.import_type.value] += 1
            self._import_stats['by_scope']['absolute' if imp.is_absolute else 'relative'] += 1
            self._import_stats['modules'].add(imp.module_name)

        # Count used vs unused imports
        usage = self.import_usage
        self._import_stats['used_count'] = len(usage['used'])
        self._import_stats['unused_count'] = len(usage['unused'])
        self._import_stats['modules'] = list(self._import_stats['modules'])

    def _calculate_code_metrics(self) -> None:
        """Calculate comprehensive code quality and complexity metrics."""
        if self._code_metrics is not None:
            return

        # Line metrics
        total_lines = len(self.lines)
        code_lines = len([line for line in self.lines if line.strip()
                         and not line.strip().startswith('#')])
        comment_lines = len(self.comments)
        blank_lines = max(0, total_lines - code_lines - comment_lines)

        # Complexity metrics
        function_count = len(self.function_names)
        class_count = len(self.class_names)
        import_count = len(self.imports)

        # Calculate cyclomatic complexity (simplified)
        complexity = 1  # Base complexity
        for node in ast.walk(self._tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        # Code quality indicators
        has_docstrings = any(
            '"""' in line or "'''" in line for line in self.lines)
        has_type_hints = any(
            ':' in line and '->' in line for line in self.lines)

        # Determine quality level
        quality_score = 0
        if has_docstrings:
            quality_score += 2
        if has_type_hints:
            quality_score += 2
        if blank_lines > 0:
            quality_score += 1
        if complexity < 10:
            quality_score += 2
        elif complexity < 20:
            quality_score += 1

        if quality_score >= 6:
            quality_level = CodeQualityLevel.EXCELLENT
        elif quality_score >= 4:
            quality_level = CodeQualityLevel.GOOD
        elif quality_score >= 2:
            quality_level = CodeQualityLevel.FAIR
        elif quality_score >= 0:
            quality_level = CodeQualityLevel.POOR
        else:
            quality_level = CodeQualityLevel.UNKNOWN

        self._code_metrics = {
            'lines': {
                'total': total_lines,
                'code': code_lines,
                'comment': comment_lines,
                'blank': blank_lines,
                'comment_ratio': comment_lines / total_lines if total_lines > 0 else 0
            },
            'complexity': {
                'cyclomatic': complexity,
                'function_count': function_count,
                'class_count': class_count,
                'import_count': import_count,
                'average_function_complexity': complexity / function_count if function_count > 0 else 0
            },
            'quality': {
                'level': quality_level,
                'score': quality_score,
                'has_docstrings': has_docstrings,
                'has_type_hints': has_type_hints,
                'import_efficiency': len(self.imports) - len(self.import_usage['unused']) if self.imports else 0
            }
        }

    def _analyze_structure(self) -> None:
        """Analyze the structural relationships in the code."""
        if self._structure_info is not None:
            return

        # Analyze nested structures by tracking parent-child relationships
        nested_functions = []
        nested_classes = []

        # Build a simple parent tracking system
        parent_map = {}
        current_parent = None

        for node in ast.walk(self._tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # Set parent for this node
                parent_map[node] = current_parent

                # Check if this is nested
                if current_parent is not None:
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        nested_functions.append(node.name)
                    elif isinstance(node, ast.ClassDef):
                        nested_classes.append(node.name)

                # Set this as current parent for children
                current_parent = node
            elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                # These don't change the nesting level for functions/classes
                pass
            elif isinstance(node, ast.Module):
                # Reset to module level
                current_parent = None

        # Analyze decorators
        decorators = []
        for node in ast.walk(self._tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.decorator_list:
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        decorators.append(decorator.id)
                    elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                        decorators.append(decorator.func.id)

        # Analyze async usage
        async_functions = [name for name in self.function_names if name in
                           [node.name for node in ast.walk(self._tree)
                            if isinstance(node, ast.AsyncFunctionDef)]]

        self._structure_info = {
            'nested': {
                'functions': nested_functions,
                'classes': nested_classes
            },
            'decorators': list(set(decorators)),
            'async': {
                'functions': async_functions,
                'count': len(async_functions)
            },
            'inheritance': self._analyze_inheritance()
        }

    def _analyze_inheritance(self) -> Dict[str, Any]:
        """Analyze class inheritance relationships."""
        inheritance_info = {}

        for node in ast.walk(self._tree):
            if isinstance(node, ast.ClassDef):
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        # Handle cases like 'module.Class'
                        parts = []
                        current = base
                        while isinstance(current, ast.Attribute):
                            parts.append(current.attr)
                            current = current.value
                        if isinstance(current, ast.Name):
                            parts.append(current.id)
                            parts.reverse()
                            bases.append('.'.join(parts))

                inheritance_info[node.name] = {
                    'bases': bases,
                    'base_count': len(bases),
                    'is_mixin': len(bases) > 1,
                    'is_leaf': True  # Will be updated below
                }

        # Mark classes that are used as bases
        for class_name, info in inheritance_info.items():
            for base_name in info['bases']:
                if base_name in inheritance_info:
                    inheritance_info[base_name]['is_leaf'] = False

        return inheritance_info

    # ==================== PROPERTIES ====================

    @property
    def tokens(self) -> List[tokenize.TokenInfo]:
        """Returns the list of tokens from the file."""
        if self._tokens is None:
            self._tokenize()
        return self._tokens

    @property
    def lines(self) -> List[str]:
        """Returns the list of lines from the file."""
        if self._lines is None:
            self._parse_lines()
        return self._lines

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
    def imports(self) -> List[ImportInfo]:
        """Returns a list of ImportInfo objects representing all import statements."""
        if self._imports is None:
            self._analyze_imports()
        return self._imports

    @property
    def import_statistics(self) -> Dict[str, Any]:
        """Returns comprehensive import statistics."""
        if self._import_stats is None:
            self._analyze_imports()
        return self._import_stats

    @property
    def used_names(self) -> Set[str]:
        """A set of all names (identifiers) used in the file."""
        names = set()

        # Add names from AST nodes
        for node in ast.walk(self._tree):
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # Handle attribute access like 'module.function'
                if isinstance(node.value, ast.Name):
                    names.add(node.value.id)
                names.add(node.attr)

        # Add imported names that are used
        for imp in self.imports:
            if imp.effective_name:
                names.add(imp.effective_name)
            if imp.module_name:
                # Add module name parts
                for part in imp.module_name.split('.'):
                    if part:
                        names.add(part)

        return names

    @property
    def import_usage(self) -> Dict[str, List[ImportInfo]]:
        """Returns used and unused imports."""
        used, unused = [], []
        for imp in self.imports:
            if imp.alias == "*" or imp.alias is None or imp.effective_name in self.used_names:
                used.append(imp)
            else:
                unused.append(imp)
        return {"used": used, "unused": unused}

    @property
    def code_metrics(self) -> Dict[str, Any]:
        """Returns comprehensive code quality metrics."""
        if self._code_metrics is None:
            self._calculate_code_metrics()
        return self._code_metrics

    @property
    def structure_info(self) -> Dict[str, Any]:
        """Returns structural analysis information."""
        if self._structure_info is None:
            self._analyze_structure()
        return self._structure_info

    @property
    def file_size(self) -> Dict[str, int]:
        """Returns file size metrics in various units."""
        content_bytes = len(self._content.encode('utf-8'))
        return {
            'bytes': content_bytes,
            'kilobytes': content_bytes // 1024,
            'characters': len(self._content),
            'lines': len(self.lines),
            'tokens': self.token_count
        }

    # ==================== DYNAMIC ANALYSIS ====================

    def _load_module(self) -> Any:
        """Dynamically loads the file as a module and returns the module object."""
        try:
            module_name = "_temp_module_" + str(abs(hash(self.file_path)))
            spec = importlib.util.spec_from_file_location(
                module_name, self.file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"Error loading module from {self.file_path}: {e}")
            return None

    def get_dynamic_class_info(self) -> List[ClassInfo]:
        """Returns detailed ClassInfo objects for all classes."""
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

    def get_dynamic_function_info(self) -> List[FunctionInfo]:
        """Returns detailed FunctionInfo objects for all functions."""
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
                    infos.append(FunctionInfo(obj, module))
                except Exception as e:
                    print(f"Error processing function {name}: {e}")
        return infos

    # ==================== ANALYSIS METHODS ====================

    def get_imports_by_type(self, import_type: ImportType) -> List[ImportInfo]:
        """Returns imports filtered by ImportType."""
        return [imp for imp in self.imports if imp.import_type == import_type]

    def get_imports_by_scope(self, is_absolute: bool) -> List[ImportInfo]:
        """Returns imports filtered by scope (absolute or relative)."""
        return [imp for imp in self.imports if imp.is_absolute == is_absolute]

    def get_unused_imports(self) -> List[ImportInfo]:
        """Returns list of unused imports."""
        return self.import_usage['unused']

    def get_used_imports(self) -> List[ImportInfo]:
        """Returns list of used imports."""
        return self.import_usage['used']

    def get_import_efficiency_score(self) -> float:
        """Returns import efficiency as a percentage."""
        if not self.imports:
            return 100.0
        return (len(self.get_used_imports()) / len(self.imports)) * 100

    def get_complexity_assessment(self) -> str:
        """Returns a human-readable complexity assessment."""
        complexity = self.code_metrics['complexity']['cyclomatic']
        if complexity <= 5:
            return "Very Low"
        elif complexity <= 10:
            return "Low"
        elif complexity <= 20:
            return "Medium"
        elif complexity <= 50:
            return "High"
        else:
            return "Very High"

    # ==================== EXPORT METHODS ====================

    def to_dict(self) -> Dict[str, Any]:
        """Returns a comprehensive dictionary representation of the analysis."""
        return {
            'file_info': {
                'path': self.file_path,
                'size': self.file_size
            },
            'code_metrics': self.code_metrics,
            'imports': {
                'statistics': self.import_statistics,
                'list': [imp.to_dict() for imp in self.imports],
                'usage': {
                    'used': [imp.to_dict() for imp in self.get_used_imports()],
                    'unused': [imp.to_dict() for imp in self.get_unused_imports()]
                }
            },
            'structure': {
                'classes': self.class_names,
                'functions': self.function_names,
                'nested': self.structure_info['nested'],
                'inheritance': self.structure_info['inheritance'],
                'decorators': self.structure_info['decorators'],
                'async': self.structure_info['async']
            },
            'tokens': {
                'count': self.token_count,
                'distribution': self.token_distribution,
                'comments': self.comments
            }
        }

    def to_json(self, indent: int = 2) -> str:
        """Returns a JSON string representation of the analysis."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def export_summary(self, output_file: Optional[str] = None) -> str:
        """Exports a human-readable summary report."""
        summary = []
        summary.append(f"File Analysis Summary: {self.file_path}")
        summary.append("=" * 60)

        # Basic metrics
        summary.append(f"\n📊 CODE METRICS:")
        summary.append(
            f"  • Total Lines: {self.code_metrics['lines']['total']}")
        summary.append(f"  • Code Lines: {self.code_metrics['lines']['code']}")
        summary.append(
            f"  • Comment Lines: {self.code_metrics['lines']['comment']}")
        summary.append(
            f"  • Blank Lines: {self.code_metrics['lines']['blank']}")
        summary.append(
            f"  • Cyclomatic Complexity: {self.code_metrics['complexity']['cyclomatic']}")
        summary.append(
            f"  • Quality Level: {self.code_metrics['quality']['level'].value.title()}")

        # Structure
        summary.append(f"\n🏗️  STRUCTURE:")
        summary.append(f"  • Classes: {len(self.class_names)}")
        summary.append(f"  • Functions: {len(self.function_names)}")
        summary.append(
            f"  • Async Functions: {self.structure_info['async']['count']}")
        summary.append(
            f"  • Nested Functions: {len(self.structure_info['nested']['functions'])}")
        summary.append(
            f"  • Nested Classes: {len(self.structure_info['nested']['classes'])}")

        # Imports
        summary.append(f"\n📦 IMPORTS:")
        summary.append(f"  • Total: {self.import_statistics['total_imports']}")
        summary.append(f"  • Used: {self.import_statistics['used_count']}")
        summary.append(f"  • Unused: {self.import_statistics['unused_count']}")
        summary.append(
            f"  • Efficiency: {self.get_import_efficiency_score():.1f}%")
        summary.append(
            f"  • Absolute: {self.import_statistics['by_scope']['absolute']}")
        summary.append(
            f"  • Relative: {self.import_statistics['by_scope']['relative']}")

        # Import types
        for import_type, count in self.import_statistics['by_type'].items():
            summary.append(
                f"    - {import_type.replace('_', ' ').title()}: {count}")

        summary_text = '\n'.join(summary)

        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(summary_text)
                print(f"Summary exported to: {output_file}")
            except Exception as e:
                print(f"Error writing summary to {output_file}: {e}")

        return summary_text

    # ==================== STRING REPRESENTATIONS ====================

    def __str__(self) -> str:
        return (f"FileInfo(path='{self.file_path}', "
                f"lines={self.code_metrics['lines']['total']}, "
                f"complexity={self.code_metrics['complexity']['cyclomatic']}, "
                f"quality={self.code_metrics['quality']['level'].value})")

    def __repr__(self) -> str:
        return f"FileInfo('{self.file_path}')"

    # ==================== LEGACY COMPATIBILITY ====================

    def print_summary(self) -> None:
        """Legacy method for printing summary (deprecated, use export_summary)."""
        print(self.export_summary())


__all__ = [
    "FileInfo",
    "CodeQualityLevel"
]
