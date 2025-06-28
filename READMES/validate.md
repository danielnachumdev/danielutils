# `@validate`

**Runtime Type Validation for Python Functions**

Protect your functions with automatic argument validation and catch type-related errors early in development.

Browse code [here](../danielutils/decorators/validate.py)

## Purpose

The `@validate` decorator provides runtime type checking for function arguments and return values based on type annotations. It helps catch type-related bugs early in development and ensures your functions are used correctly according to their type signatures.

## Key Features

- ✅ **Automatic Type Validation** - Validates arguments and return values against type annotations
- ✅ **Flexible Validation Modes** - Support for strict and non-strict validation
- ✅ **Smart Default Handling** - Properly handles `None` default values
- ✅ **Built-in Exemptions** - Automatically exempts `self`, `cls`, `*args`, `**kwargs`
- ✅ **Comprehensive Error Messages** - Clear error reporting for validation failures
- ✅ **Performance Optimized** - Minimal overhead when validation passes

## Usage Examples

### Basic Function Validation

```python
from danielutils import validate

@validate
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old"

# Valid calls
result = greet("Alice", 30)  # ✅ Works fine
print(result)  # "Hello Alice, you are 30 years old"

# Invalid calls (will raise ValidationException)
try:
    greet(123, "thirty")  # ❌ Wrong types
except Exception as e:
    print(f"Error: {e}")
```

### Functions with Default Values

```python
from danielutils import validate
from typing import Optional, List

@validate
def create_user(
    name: str,
    age: int,
    email: Optional[str] = None,
    tags: List[str] = None
) -> dict:
    if tags is None:
        tags = []
    return {
        "name": name,
        "age": age,
        "email": email,
        "tags": tags
    }

# Valid calls with defaults
user1 = create_user("Bob", 25)  # ✅ Uses defaults
user2 = create_user("Alice", 30, "alice@example.com", ["admin", "user"])  # ✅ All args

# Invalid calls
try:
    create_user("Bob", "25")  # ❌ age should be int
except Exception as e:
    print(f"Error: {e}")
```

### Complex Type Validation

```python
from danielutils import validate
from typing import Union, Dict, List, Optional

@validate
def process_data(
    data: Union[Dict[str, int], List[int]],
    threshold: Optional[float] = None
) -> List[int]:
    if isinstance(data, dict):
        return [v for v in data.values() if threshold is None or v > threshold]
    else:
        return [v for v in data if threshold is None or v > threshold]

# Valid calls
result1 = process_data({"a": 1, "b": 5, "c": 3}, 2.0)  # ✅ Dict with threshold
result2 = process_data([1, 5, 3, 8])  # ✅ List without threshold

# Invalid calls
try:
    process_data("not valid")  # ❌ Wrong type
except Exception as e:
    print(f"Error: {e}")
```

### Class Methods

```python
from danielutils import validate

class UserManager:
    def __init__(self):
        self.users = []
    
    @validate
    def add_user(self, name: str, age: int, is_active: bool = True) -> dict:
        user = {"name": name, "age": age, "is_active": is_active}
        self.users.append(user)
        return user
    
    @validate
    def get_users_by_age(self, min_age: int, max_age: Optional[int] = None) -> List[dict]:
        if max_age is None:
            max_age = float('inf')
        return [u for u in self.users if min_age <= u["age"] <= max_age]

# Usage
manager = UserManager()
user = manager.add_user("Charlie", 28, True)  # ✅ Valid
users = manager.get_users_by_age(25, 30)  # ✅ Valid
```

### Strict vs Non-Strict Validation

```python
from danielutils import validate

# Non-strict validation (default)
@validate
def flexible_function(data: list) -> int:
    return len(data)

# Strict validation
@validate(strict=True)
def strict_function(data: list) -> int:
    return len(data)

# Both work with valid types
flexible_function([1, 2, 3])  # ✅ Works
strict_function([1, 2, 3])    # ✅ Works

# Non-strict allows some flexibility
flexible_function((1, 2, 3))  # ✅ May work (tuple is sequence-like)

# Strict enforces exact types
try:
    strict_function((1, 2, 3))  # ❌ Strict mode may reject tuple
except Exception as e:
    print(f"Strict validation error: {e}")
```

## API Reference

### Decorator Signature

```python
def validate(strict: bool = False):
    """
    Decorator for runtime type validation of function arguments and return values.
    
    Args:
        strict: If True, performs stricter type checking
        
    Returns:
        Decorated function with validation
    """
```

### Validation Rules

1. **Argument Validation**: All arguments are validated against their type annotations
2. **Return Value Validation**: Return values are validated against the return type annotation
3. **Default Values**: Default values are validated when the function is defined
4. **Exempted Parameters**: `self`, `cls`, `*args`, `**kwargs` are automatically exempted
5. **None Handling**: `None` is allowed as a default value for any type

### Exception Types

The decorator raises specific exceptions for different validation failures:

- **`TypeError`** - Decorated object is not a callable function
- **`EmptyAnnotationException`** - Argument lacks type annotation
- **`InvalidDefaultValueException`** - Default value doesn't match type annotation
- **`ValidationException`** - Argument value doesn't match expected type
- **`InvalidReturnValueException`** - Return value doesn't match expected type

## Performance Considerations

- **Minimal Overhead**: Validation only occurs when the function is called
- **Early Exit**: Validation stops at the first failure
- **Caching**: Type information is cached for better performance
- **Production**: Consider disabling validation in production for maximum performance

## Best Practices

### 1. Use Clear Type Annotations

```python
# Good
@validate
def calculate_area(width: float, height: float) -> float:
    return width * height

# Avoid
@validate
def calculate_area(width, height):  # No type hints
    return width * height
```

### 2. Handle Optional Types Properly

```python
# Good
@validate
def send_email(to: str, subject: str, body: str, cc: Optional[List[str]] = None) -> bool:
    if cc is None:
        cc = []
    # ... implementation
    return True
```

### 3. Use Union Types for Flexibility

```python
# Good
@validate
def process_input(data: Union[str, bytes, List[str]]) -> str:
    if isinstance(data, bytes):
        return data.decode('utf-8')
    elif isinstance(data, list):
        return '\n'.join(data)
    return data
```

### 4. Consider Validation Granularity

```python
# For performance-critical code, validate only critical functions
@validate
def critical_business_logic(data: Dict[str, Any]) -> bool:
    # This function is critical, so validation is important
    pass

def internal_helper(data):  # No validation for internal helpers
    # This function is internal, validation might be overkill
    pass
```

## Comparison with Other Validation Libraries

| Feature            | `@validate` | `pydantic` | `marshmallow` |
| ------------------ | ----------- | ---------- | ------------- |
| Type annotations   | ✅           | ✅          | ❌             |
| Runtime validation | ✅           | ✅          | ✅             |
| Performance        | Fast        | Medium     | Medium        |
| Learning curve     | Low         | Medium     | Medium        |
| Integration        | Drop-in     | Framework  | Framework     |

---

**Note**: The `@validate` decorator is designed to be a lightweight, drop-in solution for runtime type validation that works seamlessly with Python's type annotation system.