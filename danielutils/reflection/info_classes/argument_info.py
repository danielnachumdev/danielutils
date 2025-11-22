import re
from dataclasses import dataclass
from typing import Optional, List

ARGUMENT_INFO_REGEX: re.Pattern = re.compile(
    r"(?P<kwargs>\*\*\w[\w\d]*)|(?P<args>\*(?:\w[\w\d]*)?)|(?P<kwarg_only>\/)|(?P<pname>\w[\w\d]*)\[(?P<parameters>.+)\]|(?P<name>\w[\w\d]*)(?:(?:\s*:(?P<type>[^\=\n]+))?(?:\s*=(?P<default_value>[\s\S]+))?)?")


class ArgumentInfo:
    def __init__(
            self,
            name: Optional[str],
            type: Optional[str],
            default: Optional[str],
            is_kwargs: bool,
            is_args: bool,
            is_kwargs_only: bool,
            parameters: Optional[List]
    ) -> None:
        self._name = name
        self._type = type
        self._default = default
        self._is_kwargs = is_kwargs
        self._is_args = is_args
        self._is_kwargs_only = is_kwargs_only
        self._parameters = parameters

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def type(self) -> Optional[str]:
        return self._type

    @property
    def default(self) -> Optional[str]:
        return self._default

    @property
    def is_kwargs(self) -> bool:
        return self._is_kwargs

    @property
    def is_args(self) -> bool:
        return self._is_args

    @property
    def is_kwargs_only(self) -> bool:
        return self._is_kwargs_only

    @property
    def parameters(self) -> Optional[List]:
        return self._parameters

    @property
    def is_parameterized(self) -> bool:
        return self._parameters is not None and len(self._parameters) > 0

    def __repr__(self) -> str:
        res = f"{self.__class__.__name__}(name=\"{self.name}\""
        if self.type is not None:
            res += f", type={self.type}"
        if self.default is not None:
            res += f", default={self.default}"
        if self.is_parameterized:
            res += f", parameters={self.parameters}"
        return res + ")"

    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def _parse_one(string: str) -> 'ArgumentInfo':
        string = string.strip()

        # Handle string literals (decorator context)
        if string.startswith('"') or string.startswith("'"):
            # Extract the string literal (handling escaped quotes)
            quote_char = string[0]
            # Find the matching closing quote
            i = 1
            while i < len(string):
                if string[i] == quote_char and (i == 0 or string[i-1] != '\\'):
                    # Found matching quote
                    literal_value = string[:i+1]
                    return ArgumentInfo(
                        name=None,
                        type=None,
                        default=literal_value,
                        is_kwargs=False,
                        is_args=False,
                        is_kwargs_only=False,
                        parameters=None
                    )
                i += 1
            # If no closing quote found, treat the whole string as the literal
            return ArgumentInfo(
                name=None,
                type=None,
                default=string,
                is_kwargs=False,
                is_args=False,
                is_kwargs_only=False,
                parameters=None
            )

        # Handle other literals (numbers, booleans, None, etc.) - check BEFORE regex
        # In decorator context, these are always literals, not parameter definitions
        if string:
            # Check for numeric literal (starts with digit, possibly with decimal point or negative)
            if string[0].isdigit() or (len(string) > 1 and string[0] == '-' and string[1].isdigit()):
                return ArgumentInfo(
                    name=None,
                    type=None,
                    default=string,
                    is_kwargs=False,
                    is_args=False,
                    is_kwargs_only=False,
                    parameters=None
                )
            # Check for boolean or None literals
            if string in ('True', 'False', 'None'):
                return ArgumentInfo(
                    name=None,
                    type=None,
                    default=string,
                    is_kwargs=False,
                    is_args=False,
                    is_kwargs_only=False,
                    parameters=None
                )
            # Check for list/dict literals or function calls (starts with bracket, brace, or identifier followed by paren)
            if string.startswith('[') or string.startswith('{') or string.startswith('('):
                return ArgumentInfo(
                    name=None,
                    type=None,
                    default=string,
                    is_kwargs=False,
                    is_args=False,
                    is_kwargs_only=False,
                    parameters=None
                )
            # Check for function call pattern (identifier followed by opening paren)
            # This handles cases like "some_function(1, 2)"
            if '(' in string and not string.startswith('='):
                # Check if it looks like a function call (has identifier before paren)
                parts = string.split('(', 1)
                if len(parts) == 2 and parts[0].strip() and (parts[0].strip()[0].isalpha() or parts[0].strip()[0] == '_'):
                    return ArgumentInfo(
                        name=None,
                        type=None,
                        default=string,
                        is_kwargs=False,
                        is_args=False,
                        is_kwargs_only=False,
                        parameters=None
                    )

        # Try regex matching for normal argument patterns
        m = ARGUMENT_INFO_REGEX.match(string)
        if m is None:
            raise ValueError(f"Invalid argument info string: {string}")

        kwargs, args, kwarg_only, pname, parameters, name, type, default_value = m.groups()
        type = None if type is None else type.strip()
        default_value = None if default_value is None else default_value.strip()

        return ArgumentInfo(
            name=name or pname or (args.strip("*") if args else None) or (
                kwargs.strip("*") if kwargs else None) or (kwarg_only if kwarg_only else None) or None,
            type=type,
            default=default_value,
            is_kwargs=kwargs is not None,
            is_args=args is not None,
            is_kwargs_only=kwarg_only is not None,
            parameters=[parameters]
        )

    @staticmethod
    def _strip_comments(string: str) -> str:
        """Strip comments from string while preserving string literals."""
        result = []
        in_string = False
        string_char = None
        i = 0
        while i < len(string):
            c = string[i]
            # Track string literals
            if c in {'"', "'"} and (i == 0 or string[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = c
                elif c == string_char:
                    in_string = False
                    string_char = None
                result.append(c)
            # Handle comments (only when not in string)
            elif not in_string and c == '#':
                # Skip everything from # to end of line (or end of string)
                # Keep the newline if present to preserve line structure
                while i < len(string) and string[i] != '\n':
                    i += 1
                # Include the newline if we found one
                if i < len(string) and string[i] == '\n':
                    result.append('\n')
                    i += 1
                    continue
                else:
                    # End of string, break
                    break
            else:
                result.append(c)
            i += 1
        return ''.join(result)

    @staticmethod
    def from_str(string: str) -> List['ArgumentInfo']:
        if string is None:
            return []
        string = string.strip()
        if not string:
            return []
        # Strip comments before processing
        string = ArgumentInfo._strip_comments(string).strip()
        indices = [-1]
        stack: List[str] = []
        in_string = False
        string_char = None
        for i, c in enumerate(string):
            # Track string literals
            if c in {'"', "'"} and (i == 0 or string[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = c
                elif c == string_char:
                    in_string = False
                    string_char = None
            # Track brackets, braces, and parentheses only when not in string
            elif not in_string:
                if c in {'[', ']', '{', '}', '(', ')'}:
                    if c in {'[', '{', '('}:
                        stack.append(c)
                    else:
                        # Match closing brackets/braces/parens with opening ones
                        if stack:
                            opening = stack[-1]
                            if (c == ']' and opening == '[') or \
                               (c == '}' and opening == '{') or \
                               (c == ')' and opening == '('):
                                stack.pop()
                elif len(stack) == 0:
                    if c == ",":
                        indices.append(i)
        indices.append(len(string))
        res = []
        for idx, (start, end) in enumerate(zip(indices[:-1], indices[1:])):
            substr = string[start + 1:end].strip()
            # Skip standalone * (keyword-only separator)
            if substr == "*":
                continue
            # Skip empty strings (from comment-only lines)
            if not substr:
                continue
            try:
                res.append(ArgumentInfo._parse_one(substr))
            except ValueError as e:
                raise ValueError(
                    f"Failed to parse argument {idx + 1}: {e}\n"
                    f"Argument string: {repr(substr)}\n"
                    f"Full arguments string: {repr(string)}"
                ) from e
        return res


__all__ = [
    "ArgumentInfo",
]
