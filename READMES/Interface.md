# `Interface`

**Interface Implementation for Python**

Create interface-like behavior using metaclasses and enhance your object-oriented programming with clear contracts and abstract method definitions.

> **⚠️ Educational Project Disclaimer**: This `Interface` metaclass was created as an educational exercise to learn about Python metaclasses and interface patterns. **It should NOT be used in production code**. For real-world applications, please use Python's built-in `abc.ABC` (Abstract Base Classes) from the standard library, which is more robust, well-tested, and officially supported.

Browse code [here](../danielutils/metaclasses/interface.py)

## Purpose

The `Interface` metaclass provides a way to define interfaces in Python, similar to interfaces in languages like Java or C#. It allows you to create abstract base classes that define a contract for implementing classes, ensuring that all required methods are implemented and providing better code organization and type safety.

## Key Features

- ✅ **Interface Definition** - Define clear contracts for implementing classes
- ✅ **Method Validation** - Automatic validation of required method implementations
- ✅ **Abstract Method Support** - Mark methods as abstract to enforce implementation
- ✅ **Inheritance Support** - Interfaces can inherit from other interfaces
- ✅ **Type Safety** - Enhanced type checking and IDE support
- ✅ **Clear Contracts** - Explicit definition of what implementing classes must provide

## Usage Examples

### Basic Interface Definition

```python
from danielutils import Interface

class DatabaseInterface(metaclass=Interface):
    """Interface for database operations"""
    
    def connect(self) -> bool:
        """Connect to the database"""
        ...
    
    def disconnect(self) -> None:
        """Disconnect from the database"""
        ...
    
    def execute_query(self, query: str) -> list:
        """Execute a database query"""
        ...
    
    def close(self) -> None:
        """Close the database connection"""
        ...

# Implementation
class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connected = False
    
    def connect(self) -> bool:
        print(f"Connecting to SQLite database: {self.db_path}")
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        print("Disconnecting from SQLite database")
        self.connected = False
    
    def execute_query(self, query: str) -> list:
        if not self.connected:
            raise RuntimeError("Database not connected")
        print(f"Executing query: {query}")
        return [{"result": "data"}]
    
    def close(self) -> None:
        self.disconnect()

# Usage
db = SQLiteDatabase("test.db")
db.connect()
results = db.execute_query("SELECT * FROM users")
db.close()
```

### Interface with Abstract Methods

```python
from danielutils import Interface

class PaymentProcessor(metaclass=Interface):
    """Interface for payment processing"""
    
    def process_payment(self, amount: float, currency: str) -> bool:
        """Process a payment"""
        ...
    
    def refund_payment(self, payment_id: str) -> bool:
        """Refund a payment"""
        ...
    
    def get_balance(self) -> float:
        """Get current balance"""
        ...

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.balance = 0.0
    
    def process_payment(self, amount: float, currency: str) -> bool:
        print(f"Processing credit card payment: {amount} {currency}")
        self.balance += amount
        return True
    
    def refund_payment(self, payment_id: str) -> bool:
        print(f"Processing refund for payment: {payment_id}")
        return True
    
    def get_balance(self) -> float:
        return self.balance

class PayPalProcessor(PaymentProcessor):
    def __init__(self, email: str):
        self.email = email
        self.balance = 0.0
    
    def process_payment(self, amount: float, currency: str) -> bool:
        print(f"Processing PayPal payment: {amount} {currency}")
        self.balance += amount
        return True
    
    def refund_payment(self, payment_id: str) -> bool:
        print(f"Processing PayPal refund for payment: {payment_id}")
        return True
    
    def get_balance(self) -> float:
        return self.balance

# Usage
processors = [
    CreditCardProcessor("api_key_123"),
    PayPalProcessor("user@example.com")
]

for processor in processors:
    processor.process_payment(100.0, "USD")
    print(f"Balance: {processor.get_balance()}")
```

### Interface Inheritance

```python
from danielutils import Interface

class Animal(metaclass=Interface):
    """Base interface for animals"""
    
    def make_sound(self) -> str:
        """Make a sound"""
        ...
    
    def move(self) -> str:
        """Move around"""
        ...

class Pet(Animal, metaclass=Interface):
    """Interface for pets that extends Animal"""
    
    def get_name(self) -> str:
        """Get the pet's name"""
        ...
    
    def play(self) -> str:
        """Play with the pet"""
        ...

class Dog(Pet):
    def __init__(self, name: str):
        self.name = name
    
    def make_sound(self) -> str:
        return "Woof!"
    
    def move(self) -> str:
        return "Running on four legs"
    
    def get_name(self) -> str:
        return self.name
    
    def play(self) -> str:
        return f"{self.name} is playing fetch"

class Cat(Pet):
    def __init__(self, name: str):
        self.name = name
    
    def make_sound(self) -> str:
        return "Meow!"
    
    def move(self) -> str:
        return "Walking gracefully"
    
    def get_name(self) -> str:
        return self.name
    
    def play(self) -> str:
        return f"{self.name} is chasing a laser pointer"

# Usage
pets = [Dog("Buddy"), Cat("Whiskers")]

for pet in pets:
    print(f"{pet.get_name()}: {pet.make_sound()}")
    print(f"Movement: {pet.move()}")
    print(f"Activity: {pet.play()}")
    print()
```

### Complex Interface with Properties

```python
from danielutils import Interface
from typing import List, Optional

class UserRepository(metaclass=Interface):
    """Interface for user data access"""
    
    def find_by_id(self, user_id: int) -> Optional[dict]:
        """Find user by ID"""
        ...
    
    def find_all(self) -> List[dict]:
        """Find all users"""
        ...
    
    def save(self, user: dict) -> bool:
        """Save a user"""
        ...
    
    def delete(self, user_id: int) -> bool:
        """Delete a user"""
        ...
    
    def count(self) -> int:
        """Get total number of users"""
        ...

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def find_by_id(self, user_id: int) -> Optional[dict]:
        return self.users.get(user_id)
    
    def find_all(self) -> List[dict]:
        return list(self.users.values())
    
    def save(self, user: dict) -> bool:
        if 'id' not in user:
            user['id'] = self.next_id
            self.next_id += 1
        self.users[user['id']] = user.copy()
        return True
    
    def delete(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def count(self) -> int:
        return len(self.users)

# Usage
repo = InMemoryUserRepository()

# Add users
user1 = {"name": "Alice", "email": "alice@example.com"}
user2 = {"name": "Bob", "email": "bob@example.com"}

repo.save(user1)
repo.save(user2)

print(f"Total users: {repo.count()}")
print(f"All users: {repo.find_all()}")
print(f"User 1: {repo.find_by_id(1)}")
```

### Interface with Static Methods

```python
from danielutils import Interface
from typing import Type

class Logger(metaclass=Interface):
    """Interface for logging functionality"""
    
    def log(self, message: str, level: str = "INFO") -> None:
        """Log a message"""
        ...
    
    def error(self, message: str) -> None:
        """Log an error message"""
        ...
    
    def warning(self, message: str) -> None:
        """Log a warning message"""
        ...
    
    @classmethod
    def get_instance(cls) -> 'Logger':
        """Get logger instance"""
        ...

class ConsoleLogger(Logger):
    def __init__(self, name: str):
        self.name = name
    
    def log(self, message: str, level: str = "INFO") -> None:
        print(f"[{level}] {self.name}: {message}")
    
    def error(self, message: str) -> None:
        self.log(message, "ERROR")
    
    def warning(self, message: str) -> None:
        self.log(message, "WARNING")
    
    @classmethod
    def get_instance(cls) -> 'ConsoleLogger':
        return cls("DefaultLogger")

class FileLogger(Logger):
    def __init__(self, filename: str):
        self.filename = filename
    
    def log(self, message: str, level: str = "INFO") -> None:
        with open(self.filename, 'a') as f:
            f.write(f"[{level}] {message}\n")
    
    def error(self, message: str) -> None:
        self.log(message, "ERROR")
    
    def warning(self, message: str) -> None:
        self.log(message, "WARNING")
    
    @classmethod
    def get_instance(cls) -> 'FileLogger':
        return cls("app.log")

# Usage
loggers = [ConsoleLogger("App"), FileLogger("debug.log")]

for logger in loggers:
    logger.log("Application started")
    logger.warning("This is a warning")
    logger.error("This is an error")
```

## API Reference

### Interface Metaclass

```python
class Interface(type):
    """
    Metaclass for creating interfaces in Python.
    
    Interfaces define a contract that implementing classes must follow.
    All methods in an interface must be implemented by any class that
    uses the interface as a metaclass.
    """
```

### Interface Definition Pattern

```python
class MyInterface(metaclass=Interface):
    """Documentation for the interface"""
    
    def required_method(self, param: str) -> bool:
        """Documentation for the method"""
        ...  # Abstract method (no implementation)
    
    def optional_method(self, param: int) -> str:
        """Optional method with default implementation"""
        return f"Default: {param}"  # Default implementation
```

### Implementation Pattern

```python
class MyImplementation(MyInterface):
    """Implementation of the interface"""
    
    def required_method(self, param: str) -> bool:
        # Must implement this method
        return param == "expected"
    
    # optional_method is inherited with default implementation
```

## Best Practices

### 1. Clear Interface Design

```python
# Good: Clear, focused interface
class DataProcessor(metaclass=Interface):
    def process(self, data: bytes) -> bytes:
        """Process binary data"""
        ...
    
    def validate(self, data: bytes) -> bool:
        """Validate data format"""
        ...

# Avoid: Too many responsibilities
class DataProcessor(metaclass=Interface):
    def process(self, data: bytes) -> bytes:
        ...
    def validate(self, data: bytes) -> bool:
        ...
    def compress(self, data: bytes) -> bytes:
        ...
    def encrypt(self, data: bytes) -> bytes:
        ...
    def send_email(self, to: str, subject: str) -> bool:
        ...
```

### 2. Proper Documentation

```python
class PaymentGateway(metaclass=Interface):
    """Interface for payment processing gateways.
    
    This interface defines the contract that all payment gateways
    must implement to be compatible with the payment system.
    """
    
    def authorize_payment(self, amount: float, card_token: str) -> str:
        """Authorize a payment transaction.
        
        Args:
            amount: Payment amount in currency units
            card_token: Secure token representing the payment method
            
        Returns:
            Transaction ID for the authorized payment
            
        Raises:
            PaymentError: If authorization fails
        """
        ...
```

### 3. Type Safety

```python
from typing import List, Optional, Union

class UserService(metaclass=Interface):
    def find_user(self, user_id: int) -> Optional[dict]:
        ...
    
    def find_users(self, criteria: dict) -> List[dict]:
        ...
    
    def create_user(self, user_data: dict) -> Union[dict, None]:
        ...
```

### 4. Interface Composition

```python
# Compose interfaces for complex systems
class ReadableRepository(metaclass=Interface):
    def find_by_id(self, id: int) -> Optional[dict]:
        ...
    
    def find_all(self) -> List[dict]:
        ...

class WritableRepository(metaclass=Interface):
    def save(self, entity: dict) -> bool:
        ...
    
    def delete(self, id: int) -> bool:
        ...

class FullRepository(ReadableRepository, WritableRepository, metaclass=Interface):
    """Combines read and write capabilities"""
    pass
```

## Comparison with Other Approaches

| Feature             | `Interface` | `abc.ABC` | `Protocol` |
| ------------------- | ----------- | --------- | ---------- |
| Explicit contracts  | ✅           | ✅         | ❌          |
| Method validation   | ✅           | ✅         | ❌          |
| Inheritance support | ✅           | ✅         | ✅          |
| Static analysis     | ✅           | ✅         | ✅          |
| Runtime checking    | ✅           | ✅         | ✅          |
| Learning curve      | Low         | Medium    | Medium     |

## Common Patterns

### 1. Repository Pattern

```python
class Repository(metaclass=Interface):
    def find_by_id(self, id: int) -> Optional[dict]:
        ...
    
    def save(self, entity: dict) -> bool:
        ...
    
    def delete(self, id: int) -> bool:
        ...
```

### 2. Service Pattern

```python
class UserService(metaclass=Interface):
    def create_user(self, user_data: dict) -> dict:
        ...
    
    def update_user(self, user_id: int, user_data: dict) -> dict:
        ...
    
    def delete_user(self, user_id: int) -> bool:
        ...
```

### 3. Factory Pattern

```python
class ConnectionFactory(metaclass=Interface):
    def create_connection(self, config: dict) -> 'Connection':
        ...
    
    def close_connection(self, connection: 'Connection') -> None:
        ...
```

---

**Note**: The `Interface` metaclass provides a clean and explicit way to define contracts in Python, making your code more maintainable and self-documenting while ensuring that implementing classes follow the defined contract.