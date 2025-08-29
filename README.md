[![Python package](https://github.com/danielnachumdev/danielutils/actions/workflows/python-package.yml/badge.svg)](https://github.com/danielnachumdev/danielutils/actions/workflows/python-package.yml)
[![Pylint](https://github.com/danielnachumdev/danielutils/actions/workflows/pylint.yml/badge.svg)](https://github.com/danielnachumdev/danielutils/actions/workflows/pylint.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![gitleaks](https://github.com/danielnachumdev/danielutils/actions/workflows/gitleaks.yml/badge.svg)](https://github.com/danielnachumdev/danielutils/actions/workflows/gitleaks.yml)
[![CodeQL](https://github.com/danielnachumdev/danielutils/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/danielnachumdev/danielutils/actions/workflows/github-code-scanning/codeql)

# danielutils v1.0.51

A comprehensive Python utilities library designed to enhance your development workflow with powerful tools for type safety, async programming, database operations, and much more.

**Features:**
- 🎯 **Type Safety**: Advanced type checking, validation, and typed collections
- ⚡ **Async Support**: Comprehensive async utilities and worker pools
- 🗄️ **Database Abstractions**: Multi-backend database support (SQLite, Redis, In-Memory)
- 🔄 **Retry Logic**: Configurable retry executors with multiple backoff strategies
- 📊 **Data Structures**: Enhanced collections, graphs, heaps, and algorithms
- 🎨 **Developer Experience**: Progress bars, logging, reflection, and debugging tools
- 🧮 **Academic Tools**: Probability theory and statistical functions

**Tested Python versions**: `3.8.0+`, `3.9.0`, `3.10.13`

> **Note**: This package is actively developed and subject to change. Use at your own risk!

## 🚀 Quick Start

```python
from danielutils import isoftype, validate, tlist
from danielutils.abstractions.db import DatabaseFactory
from danielutils.abstractions.db.database_definitions import TableSchema, TableColumn, ColumnType

# Type-safe list with runtime validation
numbers = tlist[int]([1, 2, 3, 4, 5])

# Function validation
@validate
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old"

# Database operations
db = DatabaseFactory.get_database("memory")  # In-memory database
with db:
    # Create a table
    schema = TableSchema(
        name="users",
        columns=[
            TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
            TableColumn(name="name", type=ColumnType.TEXT, nullable=False),
            TableColumn(name="age", type=ColumnType.INTEGER)
        ]
    )
    db.create_table(schema)
    
    # Insert data
    user_id = db.insert("users", {"name": "Alice", "age": 30})

# Advanced type checking
if isoftype(numbers, list[int]):
    print("Numbers is a list of integers!")
```

## 📚 Documentation

In the [`./READMES/`](./READMES/) folder you can find detailed documentation for key features:

### Core Features

#### [`isoftype`](./READMES/isoftype.md)
**Advanced Type Checking System**
- Runtime type validation with support for complex types
- Parametrized generics and union types
- Protocol and interface checking
- Enhanced type safety for your applications

#### [`@overload`](./READMES/overload.md)
**Function Overloading Made Easy**
- Manage multiple function signatures
- Type-safe function overloading
- Simplified API design with clear type hints

#### [`@validate`](./READMES/validate.md)
**Runtime Type Validation**
- Protect your functions with automatic argument validation
- Catch type-related errors early
- Enhanced debugging and error messages

#### [`tlist`](./READMES/tlist.md)
**Type-Safe Collections**
- Runtime type validation for lists
- Enhanced list operations with type safety
- Seamless integration with existing code

#### [`Interface`](./READMES/Interface.md)
**Python Interface Implementation**
- Create interface-like behavior using metaclasses
- Abstract class patterns
- Enhanced object-oriented programming

## 🛠️ Major Features

### Database Abstractions (`@/db`)
```python
from danielutils.abstractions.db import DatabaseFactory
from danielutils.abstractions.db.database_definitions import (
    TableSchema, TableColumn, ColumnType, SelectQuery, WhereClause, Condition, Operator
)

# Get different database backends
sqlite_db = DatabaseFactory.get_database("sqlite", db_kwargs={"db_path": "test.db"})
memory_db = DatabaseFactory.get_database("memory")

# Create table schema
schema = TableSchema(
    name="products",
    columns=[
        TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
        TableColumn(name="name", type=ColumnType.TEXT, nullable=False),
        TableColumn(name="price", type=ColumnType.FLOAT),
        TableColumn(name="category", type=ColumnType.TEXT)
    ]
)

# Use database with context manager
with memory_db:
    memory_db.create_table(schema)
    
    # Insert data
    product_id = memory_db.insert("products", {
        "name": "Laptop",
        "price": 999.99,
        "category": "Electronics"
    })
    
    # Query data
    query = SelectQuery(
        table="products",
        where=WhereClause(
            conditions=[
                Condition(column="category", operator=Operator.EQ, value="Electronics")
            ]
        )
    )
    results = memory_db.get(query)
```

### Async Programming
```python
import asyncio
from danielutils.async_ import AsyncWorkerPool, AsyncLayeredCommand

async def process_item(item: str) -> None:
    """Async function to process items"""
    await asyncio.sleep(0.1)  # Simulate work
    print(f"Processed: {item}")

async def main():
    # Async worker pool
    pool = AsyncWorkerPool("data_processor", num_workers=3, show_pbar=True)
    await pool.start()
    
    # Submit tasks
    items = ["item1", "item2", "item3", "item4", "item5"]
    for item in items:
        await pool.submit(process_item, args=(item,), name=f"process_{item}")
    
    # Wait for completion
    await pool.join()
    
    # Async command execution
    async with AsyncLayeredCommand("echo") as cmd:
        result = await cmd.execute("Hello from async command")
        print(f"Command output: {result}")

# Run the async example
asyncio.run(main())
```

### Retry Executors
```python
from danielutils.retry_executor import RetryExecutor
from danielutils.retry_executor.backoff_strategies import ExponentialBackOffStrategy

def unreliable_function() -> str:
    """Function that might fail"""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ValueError("Random failure")
    return "Success!"

# Create retry executor with exponential backoff
backoff = ExponentialBackOffStrategy(initial=1000)  # 1 second initial delay
executor = RetryExecutor(backoff_strategy=backoff)

# Execute with retry logic
result = executor.execute(unreliable_function, max_retries=3)
if result:
    print(f"Function succeeded: {result}")
else:
    print("Function failed after all retries")
```

### Data Structures
```python
from danielutils.data_structures import Graph, MinHeap, PriorityQueue
from danielutils.better_builtins import tlist, tdict
from typing import Any
from danielutils.data_structures.graph import MultiNode

# Type-safe collections
users = tlist[str](["alice", "bob", "charlie"])
config = tdict[str, Any]({"debug": True, "port": 8080})

# Advanced data structures
graph = Graph()
node_a = MultiNode("A")
node_b = MultiNode("B")
node_a.add_child(node_b)
graph.add_node(node_a)

# Priority queue with custom objects
class Task:
    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority
    
    def __lt__(self, other):
        return self.priority < other.priority

queue = PriorityQueue[Task]()
queue.push(Task("high_priority", 1))
queue.push(Task("low_priority", 3))
queue.push(Task("medium_priority", 2))

# Min heap
heap = MinHeap[int]()
heap.push(5)
heap.push(2)
heap.push(8)
heap.push(1)

print(f"Min value: {heap.peek()}")  # 1
```

### Progress Tracking
```python
from danielutils.progress_bar import ProgressBarPool, AsciiProgressBar

# Single progress bar
with AsciiProgressBar(range(100), position=0, desc="Processing") as pbar:
    for i in pbar:
        # Do some work
        import time
        time.sleep(0.01)

# Multiple progress bars
with ProgressBarPool(AsciiProgressBar, num_of_bars=2) as pool:
    # Configure individual bars
    pool[0].update(50)  # Update first bar
    pool[1].update(25)  # Update second bar
    
    # Write messages
    pool.write("Processing complete!")
```

### Reflection & Debugging
```python
from danielutils.reflection import FunctionInfo, ClassInfo
from danielutils.reflection.interpreter import is_debugging

def example_function(name: str, age: int = 25) -> str:
    """Example function for reflection"""
    return f"Hello {name}, age {age}"

# Function introspection
info = FunctionInfo(example_function, type)
print(f"Function name: {info.name}")
print(f"Parameters: {info.arguments}")
print(f"Return type: {info.return_type}")

# Class introspection
class ExampleClass:
    def __init__(self, value: int):
        self.value = value
    
    def get_value(self) -> int:
        return self.value

class_info = ClassInfo(ExampleClass)
print(f"Class methods: {[f.name for f in class_info.instance_methods]}")

# Runtime debugging detection
if is_debugging():
    print("Running in debug mode")
```

## 🎓 Academic & Research Tools

### Probability Theory
```python
from danielutils.university.probability import Distribution
from danielutils.university.probability.funcs import expected_value
from danielutils.university.probability.operator import Operator

# Create probability distributions
bernoulli = Distribution.Discrete.Ber(p=0.5)  # Bernoulli with p=0.5
binomial = Distribution.Discrete.Bin(n=10, p=0.3)  # Binomial with n=10, p=0.3

# Calculate probabilities
prob_1 = bernoulli.evaluate(1, Operator.EQ)  # P(X=1)
prob_0 = bernoulli.evaluate(0, Operator.EQ)  # P(X=0)

# Calculate expected values
expected_bernoulli = expected_value(bernoulli)
expected_binomial = expected_value(binomial)

print(f"Bernoulli P(X=1): {prob_1}")
print(f"Bernoulli E[X]: {expected_bernoulli}")
```

## 🔧 Installation

```bash
pip install danielutils
```

## 📈 Project Status

This library has evolved significantly since its initial release in September 2022:

- **2022**: Basic utilities and foundational features (v0.5.x - v0.7.x)
- **2023**: Major development with typed builtins and code quality (v0.8.x - v0.9.x)
- **2024**: Mature library with async support and advanced features (v0.9.x - v1.0.x)
- **2025**: Production-ready with database abstractions and enterprise features (v1.0.x+)

## 🤝 Contributing

Feel free to use, contribute, and improve this code! The project welcomes:

- Bug reports and feature requests
- Code contributions and improvements
- Documentation enhancements
- Test coverage improvements

## 📄 License

This project is licensed under the terms specified in the [LICENSE](./LICENSE) file.

---

**Built with ❤️ for the Python community**
