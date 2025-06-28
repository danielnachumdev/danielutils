# Singleton Decorator

The Singleton decorator provides a thread-safe implementation of the Singleton design pattern, ensuring that only one instance of a class exists throughout the application lifecycle. It's designed to be simple to use while handling complex inheritance scenarios correctly.

## Features

- **Thread-Safe**: Ensures singleton behavior in multi-threaded environments
- **Inheritance Support**: Properly handles class inheritance hierarchies
- **Automatic Instance Management**: No manual instance tracking required
- **Clean API**: Simple decorator syntax with minimal code changes
- **Instance Access**: Provides easy access to the singleton instance

## Basic Usage

### Simple Singleton

```python
from danielutils.decorators import singleton

@singleton
class DatabaseConnection:
    def __init__(self):
        self.connection_string = "default_connection"
        print("Database connection initialized")
    
    def connect(self):
        return f"Connected to {self.connection_string}"

# Create instances
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(db1 is db2)  # True - same instance
print(db1.connect())  # "Connected to default_connection"
```

### Singleton with Parameters

```python
from danielutils.decorators import singleton

@singleton
class Configuration:
    def __init__(self):
        self.settings = {}
        print("Configuration initialized")
    
    def set_setting(self, key, value):
        self.settings[key] = value
    
    def get_setting(self, key):
        return self.settings.get(key)

# First call initializes the singleton
config1 = Configuration()
config1.set_setting("debug", True)

# Second call returns the same instance
config2 = Configuration()
print(config2.get_setting("debug"))  # True
print(config1 is config2)  # True
```

## Advanced Usage

### Singleton with Inheritance

```python
from danielutils.decorators import singleton

class BaseService:
    def __init__(self):
        self.service_id = id(self)
    
    def get_id(self):
        return self.service_id

@singleton
class LoggingService(BaseService):
    def __init__(self):
        super().__init__()
        self.logs = []
    
    def log(self, message):
        self.logs.append(message)
    
    def get_logs(self):
        return self.logs.copy()

# Create instances
logger1 = LoggingService()
logger2 = LoggingService()

# Both are the same instance
print(logger1 is logger2)  # True
print(logger1.get_id() == logger2.get_id())  # True

# Logging works across references
logger1.log("First message")
logger2.log("Second message")
print(logger1.get_logs())  # ['First message', 'Second message']
```

### Singleton with Custom Initialization

```python
from danielutils.decorators import singleton

@singleton
class CacheManager:
    def __init__(self):
        self.cache = {}
        self.hit_count = 0
        self.miss_count = 0
        print("Cache manager initialized")
    
    def get(self, key):
        if key in self.cache:
            self.hit_count += 1
            return self.cache[key]
        else:
            self.miss_count += 1
            return None
    
    def set(self, key, value):
        self.cache[key] = value
    
    def get_stats(self):
        return {
            "hits": self.hit_count,
            "misses": self.miss_count,
            "size": len(self.cache)
        }

# Usage across different parts of the application
cache1 = CacheManager()
cache1.set("user:123", {"name": "John", "email": "john@example.com"})

cache2 = CacheManager()
user_data = cache2.get("user:123")
print(user_data)  # {'name': 'John', 'email': 'john@example.com'}

stats = cache1.get_stats()
print(stats)  # {'hits': 1, 'misses': 0, 'size': 1}
```

## Real-World Examples

### Application Settings

```python
from danielutils.decorators import singleton
import os

@singleton
class AppSettings:
    def __init__(self):
        self._settings = {
            "debug": os.getenv("DEBUG", "False").lower() == "true",
            "database_url": os.getenv("DATABASE_URL", "sqlite:///app.db"),
            "max_connections": int(os.getenv("MAX_CONNECTIONS", "10")),
            "timeout": int(os.getenv("TIMEOUT", "30"))
        }
    
    def get(self, key, default=None):
        return self._settings.get(key, default)
    
    def set(self, key, value):
        self._settings[key] = value
    
    def get_all(self):
        return self._settings.copy()

# Usage throughout the application
def initialize_database():
    settings = AppSettings()
    db_url = settings.get("database_url")
    max_conn = settings.get("max_connections")
    print(f"Connecting to {db_url} with max {max_conn} connections")

def handle_request():
    settings = AppSettings()
    timeout = settings.get("timeout")
    debug = settings.get("debug")
    print(f"Request timeout: {timeout}s, debug: {debug}")

# Both functions use the same settings instance
initialize_database()
handle_request()
```

### Logger Singleton

```python
from danielutils.decorators import singleton
import logging
from datetime import datetime

@singleton
class ApplicationLogger:
    def __init__(self):
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.INFO)
        
        # Create console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def debug(self, message):
        self.logger.debug(message)

# Usage across different modules
def user_service():
    logger = ApplicationLogger()
    logger.info("User service started")
    # ... user operations ...
    logger.info("User service completed")

def payment_service():
    logger = ApplicationLogger()
    logger.info("Payment service started")
    # ... payment operations ...
    logger.info("Payment service completed")

# Both services use the same logger instance
user_service()
payment_service()
```

### Database Connection Pool

```python
from danielutils.decorators import singleton
import threading
import time

@singleton
class ConnectionPool:
    def __init__(self):
        self.connections = []
        self.max_connections = 10
        self.lock = threading.Lock()
        print("Connection pool initialized")
    
    def get_connection(self):
        with self.lock:
            if len(self.connections) < self.max_connections:
                conn_id = len(self.connections) + 1
                self.connections.append(conn_id)
                print(f"Created connection {conn_id}")
                return conn_id
            else:
                print("No available connections")
                return None
    
    def release_connection(self, conn_id):
        with self.lock:
            if conn_id in self.connections:
                self.connections.remove(conn_id)
                print(f"Released connection {conn_id}")
    
    def get_pool_status(self):
        with self.lock:
            return {
                "active": len(self.connections),
                "available": self.max_connections - len(self.connections),
                "max": self.max_connections
            }

# Usage in different threads
def worker_thread(worker_id):
    pool = ConnectionPool()
    conn = pool.get_connection()
    if conn:
        print(f"Worker {worker_id} using connection {conn}")
        time.sleep(0.1)  # Simulate work
        pool.release_connection(conn)
        print(f"Worker {worker_id} released connection {conn}")

# Create multiple threads
threads = []
for i in range(5):
    thread = threading.Thread(target=worker_thread, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# Check final pool status
pool = ConnectionPool()
status = pool.get_pool_status()
print(f"Final pool status: {status}")
```

## Thread Safety

The singleton decorator is designed to be thread-safe:

```python
from danielutils.decorators import singleton
import threading
import time

@singleton
class ThreadSafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.count += 1
            return self.count
    
    def get_count(self):
        with self.lock:
            return self.count

def increment_worker():
    counter = ThreadSafeCounter()
    for _ in range(100):
        counter.increment()
        time.sleep(0.001)

# Create multiple threads
threads = []
for _ in range(5):
    thread = threading.Thread(target=increment_worker)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# Verify all threads used the same instance
counter = ThreadSafeCounter()
print(f"Final count: {counter.get_count()}")  # Should be 500
```

## Best Practices

1. **Use for Global State**: Singletons are ideal for managing global application state
2. **Thread Safety**: Always consider thread safety when designing singleton classes
3. **Lazy Initialization**: The singleton is created on first access, not at import time
4. **Avoid Overuse**: Don't use singletons for everything; prefer dependency injection when possible
5. **Clean Initialization**: Keep the `__init__` method simple and focused

## Limitations and Considerations

- **Testing**: Singletons can make unit testing more difficult
- **Global State**: Can lead to tight coupling and make code harder to reason about
- **Memory**: Singleton instances persist for the entire application lifecycle
- **Inheritance**: Complex inheritance hierarchies may require careful design

## Performance Characteristics

- **Memory Usage**: Single instance per decorated class
- **Access Speed**: O(1) instance access after initialization
- **Thread Safety**: Minimal overhead for thread synchronization
- **Initialization**: One-time cost on first access

The Singleton decorator provides a robust, thread-safe implementation of the Singleton pattern that's easy to use and handles complex scenarios correctly. 