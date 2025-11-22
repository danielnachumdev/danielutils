import inspect
import re
import ast
import logging
from dataclasses import dataclass
from typing import Type, List, Callable, Optional, Tuple, Dict, Any
from .decorator_info import DecoratorInfo
from .argument_info import ArgumentInfo

logger = logging.getLogger(__name__)


@dataclass
class FunctionComplexityStats:
    """Statistics about function complexity and structure."""
    max_indentation_level: int
    cyclomatic_complexity: int
    nesting_depth: int
    has_nested_functions: bool
    has_nested_classes: bool
    has_lambda_expressions: bool
    has_list_comprehensions: bool
    has_dict_comprehensions: bool
    has_set_comprehensions: bool
    has_generator_expressions: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "max_indentation_level": self.max_indentation_level,
            "cyclomatic_complexity": self.cyclomatic_complexity,
            "nesting_depth": self.nesting_depth,
            "has_nested_functions": self.has_nested_functions,
            "has_nested_classes": self.has_nested_classes,
            "has_lambda_expressions": self.has_lambda_expressions,
            "has_list_comprehensions": self.has_list_comprehensions,
            "has_dict_comprehensions": self.has_dict_comprehensions,
            "has_set_comprehensions": self.has_set_comprehensions,
            "has_generator_expressions": self.has_generator_expressions
        }


@dataclass
class FunctionTypeStats:
    """Statistics about function typing."""
    is_fully_typed: bool
    has_return_type: bool
    has_argument_types: bool
    typed_arguments_count: int
    total_arguments_count: int
    typing_score: float  # 0.0 to 1.0
    missing_type_arguments: List[str]
    has_generic_types: bool
    has_union_types: bool
    has_optional_types: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "is_fully_typed": self.is_fully_typed,
            "has_return_type": self.has_return_type,
            "has_argument_types": self.has_argument_types,
            "typed_arguments_count": self.typed_arguments_count,
            "total_arguments_count": self.total_arguments_count,
            "typing_score": round(self.typing_score, 2),
            "missing_type_arguments": self.missing_type_arguments,
            "has_generic_types": self.has_generic_types,
            "has_union_types": self.has_union_types,
            "has_optional_types": self.has_optional_types
        }


@dataclass
class FunctionCodeStats:
    """Statistics about function code structure."""
    total_lines: int
    code_lines: int
    comment_lines: int
    empty_lines: int
    docstring_lines: int
    average_line_length: float
    max_line_length: int
    min_line_length: int
    has_docstring: bool
    docstring_length: int
    function_signature_line: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_lines": self.total_lines,
            "code_lines": self.code_lines,
            "comment_lines": self.comment_lines,
            "empty_lines": self.empty_lines,
            "docstring_lines": self.docstring_lines,
            "average_line_length": round(self.average_line_length, 2),
            "max_line_length": self.max_line_length,
            "min_line_length": self.min_line_length,
            "has_docstring": self.has_docstring,
            "docstring_length": self.docstring_length,
            "function_signature_line": self.function_signature_line
        }


@dataclass
class FunctionStats:
    """Comprehensive function statistics."""
    complexity: FunctionComplexityStats
    typing: FunctionTypeStats
    code: FunctionCodeStats
    overall_score: float  # 0.0 to 1.0
    quality_assessment: str  # "excellent", "good", "fair", "poor"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "complexity": self.complexity.to_dict(),
            "typing": self.typing.to_dict(),
            "code": self.code.to_dict(),
            "overall_score": round(self.overall_score, 2),
            "quality_assessment": self.quality_assessment
        }


class FunctionInfo:
    FUNCTION_DEFINITION_REGEX: re.Pattern = re.compile(
        r"(?P<decorators>(?:@[\s\S]+?)+?)?\s*(?P<async>async )?def (?P<name>\w[\w\d]*)\s*\((?P<arguments>[\s\S]+?)?\)\s*(?:\s*\-\>\s*(?P<return_type>[\s\S]+?)\s*)?:(?P<body>[\s\S]+)",
        re.MULTILINE)

    def __init__(self, func: Callable, owner: Type) -> None:
        # Check for lambda functions
        if getattr(func, '__name__', None) == '<lambda>':
            raise TypeError(
                f"'{func.__name__}' is not a user defined function")

        # Check for abstract methods
        if getattr(func, '__isabstractmethod__', False):
            raise TypeError(
                f"'{func.__name__}' is not a user defined function")

        try:
            if inspect.isdatadescriptor(func):
                inspect.getsource(func.fget)  # type: ignore
                self._is_property = True
            else:
                inspect.getsource(func)
                self._is_property = False  # type: ignore
        except:
            raise TypeError(
                f"'{func.__name__}' is not a user defined function")
        self._func = func
        self._decorators: List[DecoratorInfo] = []
        self._arguments: List[ArgumentInfo] = []
        self._return_type: str = ""
        self._owner = owner
        self._source_code: str = ""
        self._ast_tree: Optional[ast.AST] = None
        self._parse_src_code()

    def _parse_src_code(self) -> None:
        f = self._func if not self.is_property else self._func.fget  # type:ignore
        self._source_code = inspect.getsource(f).strip()
        m = FunctionInfo.FUNCTION_DEFINITION_REGEX.match(self._source_code)
        if m is None:
            raise ValueError("Invalid function source code")
        decorators, async_, name, arguments, return_type, body = m.groups()
        if decorators is not None:
            for substr in decorators.strip().splitlines():
                try:
                    self._decorators.append(
                        DecoratorInfo.from_str(substr.strip()))
                except ValueError as e:
                    raise ValueError(
                        f"Failed to parse decorator for function '{name}': {e}\n"
                        f"Decorator string: {repr(substr.strip())}"
                    ) from e

        self._is_async = async_ is not None

        self._name = name
        if arguments is not None:
            try:
                all_args = ArgumentInfo.from_str(arguments)
            except ValueError as e:
                raise ValueError(
                    f"Failed to parse arguments for function '{name}': {e}\n"
                    f"Arguments string: {repr(arguments)}"
                ) from e
            # Filter out separator arguments (/, *) - they are syntax markers, not actual arguments
            self._arguments = [arg for arg in all_args if not (
                arg.is_kwargs_only and arg.name == "/") and not (arg.is_args and arg.name is None)]

        self._return_type = "None"
        if return_type is not None:
            self._return_type = return_type

        # Parse AST for detailed analysis
        try:
            self._ast_tree = ast.parse(self._source_code)
        except SyntaxError:
            self._ast_tree = None

    def _analyze_complexity(self) -> FunctionComplexityStats:
        """Analyze function complexity metrics."""
        if not self._ast_tree:
            return FunctionComplexityStats(
                max_indentation_level=0,
                cyclomatic_complexity=1,
                nesting_depth=0,
                has_nested_functions=False,
                has_nested_classes=False,
                has_lambda_expressions=False,
                has_list_comprehensions=False,
                has_dict_comprehensions=False,
                has_set_comprehensions=False,
                has_generator_expressions=False
            )

        max_indent = 0
        nesting_depth = 0
        cyclomatic = 1  # Base complexity
        has_nested_funcs = False
        has_nested_classes = False
        has_lambdas = False
        has_list_comp = False
        has_dict_comp = False
        has_set_comp = False
        has_gen_exp = False

        for node in ast.walk(self._ast_tree):
            # Calculate indentation level
            if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
                # Estimate indentation from column offset
                indent_level = node.col_offset // 4  # Assuming 4 spaces per indent
                max_indent = max(max_indent, indent_level)

            # Count complexity factors
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                cyclomatic += 1
                nesting_depth = max(nesting_depth, 1)
            elif isinstance(node, ast.BoolOp):
                cyclomatic += len(node.values) - 1
            elif isinstance(node, ast.FunctionDef):
                has_nested_funcs = True
                nesting_depth = max(nesting_depth, 2)
            elif isinstance(node, ast.ClassDef):
                has_nested_classes = True
                nesting_depth = max(nesting_depth, 2)
            elif isinstance(node, ast.Lambda):
                has_lambdas = True
            elif isinstance(node, ast.ListComp):
                has_list_comp = True
            elif isinstance(node, ast.DictComp):
                has_dict_comp = True
            elif isinstance(node, ast.SetComp):
                has_set_comp = True
            elif isinstance(node, ast.GeneratorExp):
                has_gen_exp = True

        return FunctionComplexityStats(
            max_indentation_level=max_indent,
            cyclomatic_complexity=cyclomatic,
            nesting_depth=nesting_depth,
            has_nested_functions=has_nested_funcs,
            has_nested_classes=has_nested_classes,
            has_lambda_expressions=has_lambdas,
            has_list_comprehensions=has_list_comp,
            has_dict_comprehensions=has_dict_comp,
            has_set_comprehensions=has_set_comp,
            has_generator_expressions=has_gen_exp
        )

    def _analyze_typing(self) -> FunctionTypeStats:
        """Analyze function typing statistics."""
        typed_args = sum(1 for arg in self._arguments if arg.type is not None)
        total_args = len(self._arguments)

        has_return = self._return_type != "None"
        has_arg_types = typed_args > 0
        is_fully_typed = has_return and has_arg_types and typed_args == total_args

        missing_types = [
            arg.name for arg in self._arguments if arg.type is None and arg.name]

        # Calculate typing score (0.0 to 1.0)
        typing_score = 0.0
        if total_args > 0:
            typing_score += (typed_args / total_args) * \
                0.6  # 60% weight for arguments
        if has_return:
            typing_score += 0.4  # 40% weight for return type

        # Check for advanced typing features
        has_generics = any('[' in str(
            arg.type) for arg in self._arguments if arg.type) or '[' in self._return_type
        has_unions = any('Union' in str(arg.type) or '|' in str(
            arg.type) for arg in self._arguments if arg.type) or 'Union' in self._return_type or '|' in self._return_type
        has_optionals = any('Optional' in str(
            arg.type) for arg in self._arguments if arg.type) or 'Optional' in self._return_type

        return FunctionTypeStats(
            is_fully_typed=is_fully_typed,
            has_return_type=has_return,
            has_argument_types=has_arg_types,
            typed_arguments_count=typed_args,
            total_arguments_count=total_args,
            typing_score=typing_score,
            missing_type_arguments=missing_types,
            has_generic_types=has_generics,
            has_union_types=has_unions,
            has_optional_types=has_optionals
        )

    def _analyze_code_structure(self) -> FunctionCodeStats:
        """Analyze function code structure statistics."""
        lines = self._source_code.splitlines()
        total_lines = len(lines)

        # Find function signature line
        signature_line = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') or line.strip().startswith('async def '):
                signature_line = i + 1
                break

        # Analyze lines
        code_lines = 0
        comment_lines = 0
        empty_lines = 0
        docstring_lines = 0
        line_lengths = []

        in_docstring = False
        docstring_delimiter = None

        for line in lines:
            stripped = line.strip()
            line_lengths.append(len(line))

            if not stripped:
                empty_lines += 1
                continue

            # Check for docstring start/end
            if '"""' in line or "'''" in line:
                if not in_docstring:
                    in_docstring = True
                    docstring_delimiter = '"""' if '"""' in line else "'''"
                    docstring_lines += 1
                elif docstring_delimiter is not None and docstring_delimiter in line:
                    in_docstring = False
                    docstring_delimiter = None
                else:
                    docstring_lines += 1
                continue
            elif in_docstring:
                docstring_lines += 1
                continue

            # Check for comments
            if stripped.startswith('#'):
                comment_lines += 1
            else:
                code_lines += 1

        has_docstring = docstring_lines > 0
        avg_line_length = sum(line_lengths) / \
            len(line_lengths) if line_lengths else 0
        max_line_length = max(line_lengths) if line_lengths else 0
        min_line_length = min(line_lengths) if line_lengths else 0

        return FunctionCodeStats(
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            empty_lines=empty_lines,
            docstring_lines=docstring_lines,
            average_line_length=avg_line_length,
            max_line_length=max_line_length,
            min_line_length=min_line_length,
            has_docstring=has_docstring,
            docstring_length=docstring_lines,
            function_signature_line=signature_line
        )

    def _calculate_overall_score(self, complexity: FunctionComplexityStats,
                                 typing: FunctionTypeStats,
                                 code: FunctionCodeStats) -> Tuple[float, str]:
        """Calculate overall function quality score."""
        score = 0.0

        # Complexity score (30% weight)
        if complexity.cyclomatic_complexity <= 5:
            score += 0.3
        elif complexity.cyclomatic_complexity <= 10:
            score += 0.2
        elif complexity.cyclomatic_complexity <= 20:
            score += 0.1

        if complexity.max_indentation_level <= 3:
            score += 0.1
        elif complexity.max_indentation_level <= 5:
            score += 0.05

        # Typing score (30% weight)
        score += typing.typing_score * 0.3

        # Code structure score (40% weight)
        if code.has_docstring:
            score += 0.1

        if code.total_lines <= 50:
            score += 0.1
        elif code.total_lines <= 100:
            score += 0.05

        if code.average_line_length <= 80:
            score += 0.1
        elif code.average_line_length <= 120:
            score += 0.05

        if code.empty_lines > 0:  # Some whitespace is good
            score += 0.05

        if code.comment_lines > 0:
            score += 0.05

        # Determine quality level
        if score >= 0.8:
            quality = "excellent"
        elif score >= 0.6:
            quality = "good"
        elif score >= 0.4:
            quality = "fair"
        else:
            quality = "poor"

        return score, quality

    @property
    def stats(self) -> FunctionStats:
        """Returns comprehensive function statistics."""
        # TODO: FunctionInfo.stats property is not yet ready for production use
        # This functionality is experimental and may not provide accurate results
        # The complexity analysis, typing analysis, and code structure analysis
        # need further testing and refinement before being considered stable
        logger.warning(
            "FunctionInfo.stats property is experimental and not yet ready for production use")

        complexity = self._analyze_complexity()
        typing = self._analyze_typing()
        code = self._analyze_code_structure()
        overall_score, quality = self._calculate_overall_score(
            complexity, typing, code)

        return FunctionStats(
            complexity=complexity,
            typing=typing,
            code=code,
            overall_score=overall_score,
            quality_assessment=quality
        )

    @property
    def source_code(self) -> str:
        """Returns the function's source code."""
        return self._source_code

    def __str__(self) -> str:
        # body = json.dumps({
        #     "name": self.name,
        #     "decorators": self.decorators,
        #     "arguments": self.arguments
        # }, default=str, indent=4)
        return f"{self.__class__.__name__}(name=\"{self.name}\", decorators={self.decorators}, arguments={self.arguments})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name=\"{self.name}\")"

    @property
    def is_async(self) -> bool:
        return self._is_async

    @property
    def is_inherited(self) -> bool:
        return self._func in set(self._owner.__dict__.keys())

    @property
    def is_class_method(self) -> bool:
        return "classmethod" in set(d.name for d in self.decorators)

    @property
    def is_static_method(self) -> bool:
        return "staticmethod" in set(d.name for d in self.decorators)

    @property
    def is_instance_method(self) -> bool:
        return not self.is_class_method and not self.is_static_method

    @property
    def is_abstract(self) -> bool:
        return getattr(self._func, '__isabstractmethod__', False)

    @property
    def is_property(self) -> bool:
        return self._is_property

    @property
    def name(self) -> str:
        return self._name

    @property
    def return_type(self) -> str:
        return self._return_type

    @property
    def arguments(self) -> List[ArgumentInfo]:
        return self._arguments

    @property
    def decorators(self) -> List[DecoratorInfo]:
        return self._decorators


__all__ = [
    "FunctionInfo",
    "FunctionStats",
    "FunctionComplexityStats",
    "FunctionTypeStats",
    "FunctionCodeStats",
]
