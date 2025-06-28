# `isoftype`

**Advanced Type Checking for Python**

Check if an object is of a given type or any of its subtypes with support for complex type scenarios including parametrized generics, unions, and nested structures.

Browse code [here](../danielutils/functions/isoftype.py)

## Purpose

The `isoftype` function provides comprehensive type checking capabilities that go beyond Python's built-in `isinstance()`. It solves the limitation of `isinstance()` not supporting parametrized generics and provides flexible type checking for complex scenarios including nested structures, unions, generics, and callable types.

## Key Features

- ✅ **Parametrized Generics Support** - Unlike `isinstance()`, supports `list[int]`, `dict[str, Any]`, etc.
- ✅ **Union Type Handling** - Check against `Union[int, str]` or `int | str`
- ✅ **Nested Structure Validation** - Handle complex nested lists, tuples, dictionaries
- ✅ **Callable Type Checking** - Validate functions, methods, and lambda expressions
- ✅ **Literal Type Support** - Check against literal types like `Literal["a", "b"]`
- ✅ **Protocol & Interface Support** - Validate against structural types
- ✅ **Flexible Mode Options** - Strict and non-strict validation modes

## Comparison with `isinstance()`

| Feature               | `isinstance()` | `isoftype()` |
| --------------------- | -------------- | ------------ |
| Basic types           | ✅              | ✅            |
| Subtypes              | ✅              | ✅            |
| Union types           | ❌              | ✅            |
| Parametrized generics | ❌              | ✅            |
| Nested structures     | ❌              | ✅            |
| Callable types        | ❌              | ✅            |
| Literal types         | ❌              | ✅            |
| Protocol types        | ❌              | ✅            |

## Usage Examples

### Basic Type Checking (Compatible with `isinstance`)

```python
from danielutils import isoftype

# Simple type checks
assert isoftype(42, int) == True
assert isoftype("Hello", str) == True
assert isoftype([1, 2, 3], list) == True
assert isoftype({"key": "value"}, dict) == True
assert isoftype(3.14, float) == True

# Subtype checking
class Shape:
    pass

class Circle(Shape):
    pass

class Rectangle(Shape):
    pass

assert isoftype(Circle(), Shape) == True
assert isoftype(Rectangle(), Shape) == True
```

### Advanced Type Checking (Beyond `isinstance`)

```python
from typing import Union, Iterable, Callable
from danielutils import isoftype

# Union types
assert isoftype(42, Union[int, str]) == True
assert isoftype("Hello", Union[int, str]) == True
assert isoftype(3.14, Union[float, bool]) == True

# Parametrized generics (NOT supported by isinstance)
assert isoftype([1, 2, 3], list[int]) == True
assert isoftype(["a", "b"], list[str]) == True
assert isoftype({"key": "value"}, dict[str, str]) == True
assert isoftype({1.0, 2.0}, set[float]) == True

# Iterable types
assert isoftype([1, 2, 3], Iterable[int]) == True
assert isoftype(("apple", "banana"), Iterable[str]) == True

# Callable types
def example_func(x: int) -> str:
    return str(x)

assert isoftype(example_func, Callable[[int], str]) == True
assert isoftype(lambda x: x * 2, Callable[[int], int]) == True
```

### Complex Nested Structures

```python
from typing import Dict, List, Optional
from danielutils import isoftype

# Nested list structures
nested_list = [[1, 2], [3, 4], [5, 6]]
assert isoftype(nested_list, list[list[int]]) == True

# Complex dictionary structures
complex_dict = {
    "users": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ],
    "settings": {"debug": True, "port": 8080}
}

# Check against complex type annotations
UserDict = Dict[str, Union[int, str]]
SettingsDict = Dict[str, Union[bool, int]]
ComplexType = Dict[str, Union[List[UserDict], SettingsDict]]

assert isoftype(complex_dict, ComplexType) == True
```

### Optional and None Handling

```python
from typing import Optional
from danielutils import isoftype

# Optional types
assert isoftype(42, Optional[int]) == True
assert isoftype(None, Optional[int]) == True
assert isoftype("hello", Optional[str]) == True

# None type specifically
assert isoftype(None, type(None)) == True
```

## API Reference

### Function Signature

```python
def isoftype(
    obj: Any, 
    target_type: Any, 
    strict: bool = False
) -> bool:
    """
    Check if an object is of a given type or any of its subtypes.
    
    Args:
        obj: The object to check
        target_type: The target type to check against
        strict: If True, performs stricter type checking
        
    Returns:
        bool: True if object matches the target type, False otherwise
    """
```

### Parameters

- **`obj`** - The object to type check
- **`target_type`** - The target type (can be a type, Union, generic, etc.)
- **`strict`** - Optional boolean for stricter validation mode

### Return Value

Returns `True` if the object matches the target type, `False` otherwise.

## Performance Considerations

- For basic types and subtypes, `isoftype()` has similar performance to `isinstance()`
- Complex type checking (generics, unions, nested structures) requires additional processing
- Use `strict=True` for better performance when exact type matching is sufficient

## Error Handling

The function gracefully handles edge cases and provides informative warnings for ambiguous scenarios:

```python
# Ambiguous cases (provides warnings)
isoftype([1, "2", 3], list[int])  # Warning: mixed types in list
isoftype(None, int)  # Returns False, no error
```

---

**Note**: This function is designed to be a drop-in replacement for `isinstance()` while providing extended functionality for complex type checking scenarios.