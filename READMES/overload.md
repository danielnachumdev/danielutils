# `@overload`

**Function Overloading for Python**

Manage multiple function signatures with ease and provide clear type hints for different argument combinations.

Browse code [here](../danielutils/decorators/overload.py)

## Purpose

The `@overload` decorator provides a clean and type-safe way to define function overloads in Python. It allows you to specify multiple function signatures for the same function, enabling better IDE support, clearer documentation, and improved type checking while maintaining a single implementation.

## Key Features

- ✅ **Multiple Signatures** - Define multiple function signatures for the same function
- ✅ **Type Safety** - Full support for complex type annotations and generics
- ✅ **IDE Support** - Enhanced autocomplete and type hints in modern IDEs
- ✅ **Clean Implementation** - Single implementation with multiple overload declarations
- ✅ **Flexible Patterns** - Support for various overloading patterns and use cases
- ✅ **Static Analysis** - Compatible with mypy and other static type checkers

## Usage Examples

### Basic Function Overloading

```python
from danielutils import overload
from typing import Union, List

@overload
def process_data(data: str) -> str:
    """Process string data"""
    ...

@overload
def process_data(data: int) -> int:
    """Process integer data"""
    ...

@overload
def process_data(data: List[str]) -> List[str]:
    """Process list of strings"""
    ...

def process_data(data: Union[str, int, List[str]]) -> Union[str, int, List[str]]:
    """Implementation for all overloads"""
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, int):
        return data * 2
    elif isinstance(data, list):
        return [item.upper() for item in data]
    else:
        raise TypeError(f"Unsupported type: {type(data)}")

# Usage with different types
result1 = process_data("hello")      # Returns: "HELLO"
result2 = process_data(42)           # Returns: 84
result3 = process_data(["a", "b"])   # Returns: ["A", "B"]
```

### Mathematical Operations Overloading

```python
from danielutils import overload
from typing import Union, List

@overload
def add_values(a: int, b: int) -> int:
    """Add two integers"""
    ...

@overload
def add_values(a: float, b: float) -> float:
    """Add two floats"""
    ...

@overload
def add_values(a: str, b: str) -> str:
    """Concatenate two strings"""
    ...

@overload
def add_values(a: List[int], b: List[int]) -> List[int]:
    """Add two lists element-wise"""
    ...

def add_values(a: Union[int, float, str, List[int]], 
               b: Union[int, float, str, List[int]]) -> Union[int, float, str, List[int]]:
    """Implementation for all overloads"""
    if isinstance(a, int) and isinstance(b, int):
        return a + b
    elif isinstance(a, float) and isinstance(b, float):
        return a + b
    elif isinstance(a, str) and isinstance(b, str):
        return a + b
    elif isinstance(a, list) and isinstance(b, list):
        return [x + y for x, y in zip(a, b)]
    else:
        raise TypeError(f"Cannot add {type(a)} and {type(b)}")

# Usage examples
print(add_values(5, 3))                    # 8
print(add_values(3.14, 2.86))              # 6.0
print(add_values("Hello ", "World"))       # "Hello World"
print(add_values([1, 2, 3], [4, 5, 6]))   # [5, 7, 9]
```

### Constructor-Style Overloading

```python
from danielutils import overload
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class User:
    name: str
    age: int
    email: Optional[str] = None

@overload
def create_user(name: str, age: int) -> User:
    """Create user with name and age"""
    ...

@overload
def create_user(name: str, age: int, email: str) -> User:
    """Create user with name, age, and email"""
    ...

@overload
def create_user(user_data: Dict[str, Any]) -> User:
    """Create user from dictionary"""
    ...

def create_user(name_or_data: Union[str, Dict[str, Any]], 
                age: Optional[int] = None, 
                email: Optional[str] = None) -> User:
    """Implementation for all overloads"""
    if isinstance(name_or_data, str):
        return User(name=name_or_data, age=age, email=email)
    elif isinstance(name_or_data, dict):
        return User(**name_or_data)
    else:
        raise TypeError(f"Invalid argument type: {type(name_or_data)}")

# Usage examples
user1 = create_user("Alice", 25)                           # User(name="Alice", age=25, email=None)
user2 = create_user("Bob", 30, "bob@example.com")         # User(name="Bob", age=30, email="bob@example.com")
user3 = create_user({"name": "Charlie", "age": 35})       # User(name="Charlie", age=35, email=None)
```

### Generic Type Overloading

```python
from danielutils import overload
from typing import TypeVar, Generic, List, Dict, Any

T = TypeVar('T')

@overload
def convert_data(data: List[T]) -> List[str]:
    """Convert list of any type to list of strings"""
    ...

@overload
def convert_data(data: Dict[str, T]) -> Dict[str, str]:
    """Convert dictionary values to strings"""
    ...

@overload
def convert_data(data: T) -> str:
    """Convert single value to string"""
    ...

def convert_data(data: Union[List[Any], Dict[str, Any], Any]) -> Union[List[str], Dict[str, str], str]:
    """Implementation for all overloads"""
    if isinstance(data, list):
        return [str(item) for item in data]
    elif isinstance(data, dict):
        return {key: str(value) for key, value in data.items()}
    else:
        return str(data)

# Usage examples
print(convert_data([1, 2, 3]))                    # ["1", "2", "3"]
print(convert_data({"a": 1, "b": 2}))             # {"a": "1", "b": "2"}
print(convert_data(42))                           # "42"
```

### Complex Type Patterns

```python
from danielutils import overload
from typing import Union, Optional, Callable, Any

@overload
def transform_data(data: str, transform: Callable[[str], str]) -> str:
    """Transform string data"""
    ...

@overload
def transform_data(data: List[str], transform: Callable[[str], str]) -> List[str]:
    """Transform list of strings"""
    ...

@overload
def transform_data(data: str, transform: None = None) -> str:
    """Transform string with default transformation"""
    ...

def transform_data(data: Union[str, List[str]], 
                  transform: Optional[Callable[[str], str]] = None) -> Union[str, List[str]]:
    """Implementation for all overloads"""
    if transform is None:
        transform = lambda x: x.upper()
    
    if isinstance(data, str):
        return transform(data)
    elif isinstance(data, list):
        return [transform(item) for item in data]
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")

# Usage examples
result1 = transform_data("hello", lambda x: x.upper())           # "HELLO"
result2 = transform_data(["a", "b"], lambda x: x.upper())       # ["A", "B"]
result3 = transform_data("world")                               # "WORLD" (default transform)
```

## API Reference

### Decorator Signature

```python
def overload(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator for function overloading.
    
    Args:
        func: The function to overload
        
    Returns:
        Decorated function with overload support
    """
```

### Overload Pattern

```python
# 1. Define overload signatures (with ... as implementation)
@overload
def function_name(arg1: Type1, arg2: Type2) -> ReturnType1:
    """Documentation for this overload"""
    ...

@overload
def function_name(arg1: Type3, arg2: Type4) -> ReturnType2:
    """Documentation for this overload"""
    ...

# 2. Define the actual implementation
def function_name(arg1: Union[Type1, Type3], arg2: Union[Type2, Type4]) -> Union[ReturnType1, ReturnType2]:
    """Implementation for all overloads"""
    # Actual implementation here
    pass
```

## Best Practices

### 1. Clear Documentation

```python
@overload
def calculate_area(width: float, height: float) -> float:
    """Calculate area of a rectangle"""
    ...

@overload
def calculate_area(radius: float) -> float:
    """Calculate area of a circle"""
    ...

def calculate_area(width_or_radius: float, height: Optional[float] = None) -> float:
    """Calculate area of rectangle or circle"""
    if height is not None:
        return width_or_radius * height  # Rectangle
    else:
        import math
        return math.pi * width_or_radius ** 2  # Circle
```

### 2. Type Safety

```python
from typing import Union, Optional

# Good: Clear type unions
@overload
def process(item: str) -> str:
    ...

@overload
def process(item: int) -> int:
    ...

def process(item: Union[str, int]) -> Union[str, int]:
    # Implementation
    pass

# Avoid: Too broad types
def process(item: Any) -> Any:  # Too permissive
    pass
```

### 3. Consistent Patterns

```python
# Good: Consistent parameter ordering
@overload
def create_object(name: str, value: int) -> Object:
    ...

@overload
def create_object(name: str, value: str) -> Object:
    ...

# Avoid: Inconsistent patterns
@overload
def create_object(value: int, name: str) -> Object:  # Different order
    ...
```

### 4. Error Handling

```python
def process_data(data: Union[str, int, List[str]]) -> Union[str, int, List[str]]:
    """Implementation with proper error handling"""
    try:
        if isinstance(data, str):
            return data.upper()
        elif isinstance(data, int):
            return data * 2
        elif isinstance(data, list):
            return [item.upper() for item in data]
        else:
            raise TypeError(f"Unsupported type: {type(data)}")
    except Exception as e:
        raise ValueError(f"Failed to process data: {e}")
```

## Comparison with Other Approaches

| Feature          | `@overload` | `functools.singledispatch` | Manual Type Checking |
| ---------------- | ----------- | -------------------------- | -------------------- |
| Type hints       | ✅           | ❌                          | ✅                    |
| IDE support      | ✅           | ❌                          | ✅                    |
| Static analysis  | ✅           | ❌                          | ✅                    |
| Runtime dispatch | ❌           | ✅                          | ✅                    |
| Learning curve   | Low         | Medium                     | Low                  |
| Code clarity     | High        | Medium                     | Low                  |

## Common Patterns

### 1. Optional Parameters

```python
@overload
def configure(host: str, port: int) -> Config:
    ...

@overload
def configure(host: str, port: int, timeout: int) -> Config:
    ...

def configure(host: str, port: int, timeout: Optional[int] = None) -> Config:
    # Implementation
    pass
```

### 2. Union Types

```python
@overload
def serialize(data: str) -> bytes:
    ...

@overload
def serialize(data: dict) -> bytes:
    ...

def serialize(data: Union[str, dict]) -> bytes:
    # Implementation
    pass
```

### 3. Generic Types

```python
T = TypeVar('T')

@overload
def convert(data: List[T]) -> List[str]:
    ...

@overload
def convert(data: T) -> str:
    ...

def convert(data: Union[List[Any], Any]) -> Union[List[str], str]:
    # Implementation
    pass
```

---

**Note**: The `@overload` decorator is designed to work seamlessly with static type checkers and modern IDEs, providing enhanced development experience while maintaining clean, readable code.