# `tlist`

**Type-Safe Lists with Runtime Validation**

Enhanced list implementation with runtime type validation to ensure type safety and catch type-related errors early.

Browse code [here](../danielutils/better_builtins/typed_builtins/tlist.py)

## Purpose

The `tlist` class provides a type-safe alternative to Python's built-in `list` with runtime type validation. It ensures that only elements of the specified type can be added to the list, helping catch type-related bugs early in development and providing better code reliability.

## Key Features

- ✅ **Runtime Type Validation** - Validates all elements against the specified type
- ✅ **Drop-in Replacement** - Compatible with most list operations and methods
- ✅ **Generic Type Support** - Works with any type including complex generics
- ✅ **Performance Optimized** - Minimal overhead when types are correct
- ✅ **Clear Error Messages** - Informative error reporting for type violations
- ✅ **Iteration Support** - Full support for iteration, slicing, and list comprehensions

## Usage Examples

### Basic Type-Safe Lists

```python
from danielutils import tlist

# Create type-safe lists
numbers = tlist[int]([1, 2, 3, 4, 5])
names = tlist[str](["Alice", "Bob", "Charlie"])
prices = tlist[float]([19.99, 29.99, 39.99])

# Valid operations
numbers.append(6)  # ✅ Valid
names.extend(["David", "Eve"])  # ✅ Valid
prices.insert(0, 9.99)  # ✅ Valid

# Invalid operations (will raise TypeError)
try:
    numbers.append("not a number")  # ❌ TypeError
except TypeError as e:
    print(f"Error: {e}")

try:
    names.append(123)  # ❌ TypeError
except TypeError as e:
    print(f"Error: {e}")
```

### Complex Type Support

```python
from danielutils import tlist
from typing import Dict, List, Union, Optional

# Lists of complex types
user_dicts = tlist[Dict[str, str]]([
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
])

# Lists with Union types
mixed_data = tlist[Union[int, str, float]]([1, "hello", 3.14, 42])

# Lists with Optional types
optional_values = tlist[Optional[str]](["value1", None, "value3"])

# Nested lists
matrix = tlist[List[int]]([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# All operations work as expected
user_dicts.append({"name": "Charlie", "email": "charlie@example.com"})  # ✅ Valid
mixed_data.extend([100, "world", 2.718])  # ✅ Valid
```

### List Operations and Methods

```python
from danielutils import tlist

# Create and populate
numbers = tlist[int]()
numbers.extend([1, 2, 3, 4, 5])

# Standard list operations
print(len(numbers))  # 5
print(numbers[0])    # 1
print(numbers[-1])   # 5

# Slicing
subset = numbers[1:4]  # tlist[int]([2, 3, 4])
print(subset)

# List comprehensions
squares = tlist[int]([x**2 for x in numbers])
print(squares)  # tlist[int]([1, 4, 9, 16, 25])

# Sorting and reversing
numbers.sort(reverse=True)
print(numbers)  # tlist[int]([5, 4, 3, 2, 1])

# Filtering
even_numbers = tlist[int]([x for x in numbers if x % 2 == 0])
print(even_numbers)  # tlist[int]([4, 2])
```

### Custom Classes and Objects

```python
from danielutils import tlist
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str

# Create a type-safe list of User objects
users = tlist[User]([
    User("Alice", 25, "alice@example.com"),
    User("Bob", 30, "bob@example.com")
])

# Add new users
users.append(User("Charlie", 35, "charlie@example.com"))  # ✅ Valid

# Invalid operation
try:
    users.append({"name": "Invalid", "age": 40, "email": "invalid@example.com"})  # ❌ TypeError
except TypeError as e:
    print(f"Error: {e}")

# Iterate and process
for user in users:
    print(f"{user.name} ({user.age}) - {user.email}")
```

### Error Handling and Validation

```python
from danielutils import tlist

# Create a list with initial validation
try:
    mixed_list = tlist[int]([1, 2, "three", 4])  # ❌ TypeError at creation
except TypeError as e:
    print(f"Creation error: {e}")

# Create empty list and add items
numbers = tlist[int]()
numbers.append(1)  # ✅ Valid
numbers.append(2)  # ✅ Valid

try:
    numbers.append("three")  # ❌ TypeError
except TypeError as e:
    print(f"Append error: {e}")

# Bulk operations with validation
try:
    numbers.extend([3, 4, "five", 6])  # ❌ TypeError
except TypeError as e:
    print(f"Extend error: {e}")

# Valid bulk operation
numbers.extend([3, 4, 5, 6])  # ✅ Valid
print(numbers)  # tlist[int]([1, 2, 3, 4, 5, 6])
```

### Performance Considerations

```python
from danielutils import tlist
import time

# Performance comparison
def benchmark_list_operations():
    # Regular list
    regular_list = []
    start = time.time()
    for i in range(10000):
        regular_list.append(i)
    regular_time = time.time() - start
    
    # Type-safe list
    safe_list = tlist[int]()
    start = time.time()
    for i in range(10000):
        safe_list.append(i)
    safe_time = time.time() - start
    
    print(f"Regular list: {regular_time:.4f}s")
    print(f"Type-safe list: {safe_time:.4f}s")
    print(f"Overhead: {((safe_time - regular_time) / regular_time) * 100:.2f}%")

# Run benchmark
benchmark_list_operations()
```

## API Reference

### Class Signature

```python
class tlist(Generic[T]):
    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        """
        Initialize a type-safe list.
        
        Args:
            iterable: Optional iterable to initialize the list with
            
        Raises:
            TypeError: If any element in iterable doesn't match the specified type
        """
```

### Supported Operations

The `tlist` class supports all standard list operations:

- **Creation**: `tlist[int]([1, 2, 3])`
- **Appending**: `append(item)`, `extend(iterable)`, `insert(index, item)`
- **Removal**: `remove(item)`, `pop(index)`, `clear()`
- **Access**: `__getitem__(index)`, `__setitem__(index, item)`, `__delitem__(index)`
- **Search**: `index(item)`, `count(item)`, `__contains__(item)`
- **Modification**: `sort()`, `reverse()`, `copy()`
- **Iteration**: `__iter__()`, `__len__()`, `__str__()`, `__repr__()`

### Type Validation

The class validates types using the `isoftype` function, which provides:

- Support for complex types (Union, Optional, generics)
- Subtype checking
- Protocol and interface validation
- Flexible validation modes

## Best Practices

### 1. Use Clear Type Annotations

```python
# Good
users = tlist[User]()
numbers = tlist[int]([1, 2, 3])

# Avoid
users = tlist([])  # No type information
```

### 2. Handle Type Errors Gracefully

```python
def safe_append(lst: tlist[int], value) -> bool:
    try:
        lst.append(value)
        return True
    except TypeError:
        print(f"Cannot append {type(value).__name__} to list of integers")
        return False
```

### 3. Use for Data Validation

```python
def validate_user_data(data: List[Dict]) -> tlist[User]:
    """Convert and validate user data"""
    users = tlist[User]()
    for item in data:
        try:
            user = User(**item)
            users.append(user)
        except (TypeError, KeyError) as e:
            print(f"Invalid user data: {e}")
    return users
```

### 4. Combine with Other Type-Safe Collections

```python
from danielutils import tlist, tdict, tset

# Type-safe data structures
users = tlist[User]()
user_cache = tdict[int, User]()
user_ids = tset[int]()

# Consistent type safety across collections
```

## Comparison with Regular Lists

| Feature            | `list` | `tlist`                |
| ------------------ | ------ | ---------------------- |
| Type safety        | ❌      | ✅                      |
| Runtime validation | ❌      | ✅                      |
| Performance        | Fast   | Fast (with validation) |
| Error detection    | Late   | Early                  |
| IDE support        | Basic  | Enhanced               |
| Learning curve     | None   | Minimal                |

## Migration Guide

### From Regular Lists

```python
# Before
numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie"]

# After
from danielutils import tlist
numbers = tlist[int]([1, 2, 3, 4, 5])
names = tlist[str](["Alice", "Bob", "Charlie"])
```

### Gradual Migration

```python
# Start with critical data
critical_data = tlist[User]()

# Keep regular lists for simple cases
simple_data = [1, 2, 3, 4, 5]
```

---

**Note**: `tlist` is designed to be a drop-in replacement for `list` while providing enhanced type safety and better error detection during development.
