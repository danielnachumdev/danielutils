# Retry Executor

The Retry Executor provides a robust mechanism for handling transient failures with configurable backoff strategies. It's designed to automatically retry operations that may fail temporarily, such as network requests, database operations, or external API calls.

## Features

- **Multiple Backoff Strategies**: Choose from constant, exponential, linear, multiplicative, and functional backoff patterns
- **Configurable Retry Limits**: Set maximum retry attempts per operation
- **Exception Callbacks**: Handle exceptions during retry attempts
- **Context Manager Support**: Use with `with` statements for clean resource management
- **Async Support**: Both synchronous and asynchronous retry executors available

## Basic Usage

### Synchronous Retry Executor

```python
from danielutils.retry_executor import RetryExecutor
from danielutils.retry_executor.backoff_strategies import ConstantBackOffStrategy

# Create a retry executor with constant 1-second delays
retry_executor = RetryExecutor(ConstantBackOffStrategy(1000))

def fetch_data():
    # Simulate a potentially failing operation
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Network error")
    return "Data retrieved successfully"

# Execute with retry logic
result = retry_executor.execute(fetch_data, max_retries=3)
print(result)  # "Data retrieved successfully" or None if all retries failed
```

### Using as Context Manager

```python
from danielutils.retry_executor import RetryExecutor
from danielutils.retry_executor.backoff_strategies import ExponentialBackOffStrategy

def risky_operation():
    import random
    if random.random() < 0.8:
        raise ValueError("Temporary failure")
    return "Success!"

# Using context manager
with RetryExecutor(ExponentialBackOffStrategy(1000)) as executor:
    result = executor.execute(risky_operation, max_retries=5)
    if result:
        print(f"Operation succeeded: {result}")
    else:
        print("All retry attempts failed")
```

## Backoff Strategies

### Constant Backoff

Always waits the same amount of time between retries.

```python
from danielutils.retry_executor.backoff_strategies import ConstantBackOffStrategy

# Wait 2 seconds between each retry
strategy = ConstantBackOffStrategy(2000)  # 2000 milliseconds
```

### Exponential Backoff

Increases delay exponentially with each retry attempt.

```python
from danielutils.retry_executor.backoff_strategies import ExponentialBackOffStrategy

# Starts with 1 second, then 2, 4, 8, 16... seconds
strategy = ExponentialBackOffStrategy(1000)  # Base delay in milliseconds
```

### Linear Backoff

Increases delay linearly with each retry attempt.

```python
from danielutils.retry_executor.backoff_strategies import LinerBackoffStrategy

# Starts with 1 second, then 2, 3, 4, 5... seconds
strategy = LinerBackoffStrategy(1000, 1000)  # Initial delay, additive term
```

### Multiplicative Backoff

Multiplies the delay by the attempt number.

```python
from danielutils.retry_executor.backoff_strategies import MultiplicativeBackoff

# Starts with 1 second, then 2, 3, 4, 5... seconds
strategy = MultiplicativeBackoff(1000)  # Base delay in milliseconds
```

### Functional Backoff

Custom backoff function for complex scenarios.

```python
from danielutils.retry_executor.backoff_strategies import FunctionalBackoffStrategy
import math

# Custom backoff: 1s, 2s, 4s, 8s, 16s...
def custom_backoff(attempt: int) -> float:
    return 1000 * (2 ** attempt)  # Returns milliseconds

strategy = FunctionalBackoffStrategy(custom_backoff)
```

### No Backoff

Immediate retry without any delay.

```python
from danielutils.retry_executor.backoff_strategies import NoBackOffStrategy

strategy = NoBackOffStrategy()  # No delay between retries
```

## Exception Handling

### Exception Callbacks

Handle exceptions during retry attempts with custom callbacks.

```python
from danielutils.retry_executor import RetryExecutor
from danielutils.retry_executor.backoff_strategies import ConstantBackOffStrategy

def log_exception(exception):
    print(f"Retry attempt failed: {type(exception).__name__}: {exception}")

def unreliable_api_call():
    import random
    if random.random() < 0.6:
        raise ConnectionError("API temporarily unavailable")
    return {"status": "success"}

executor = RetryExecutor(ConstantBackOffStrategy(1000))
result = executor.execute(
    unreliable_api_call, 
    max_retries=3, 
    exception_callback=log_exception
)
```

## Async Retry Executor

For asynchronous operations, use the `AsyncRetryExecutor`:

```python
import asyncio
from danielutils.async_ import AsyncRetryExecutor
from danielutils.async_.time_strategy import LinearTimeStrategy, ConstantTimeStrategy

async def async_operation():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Async operation failed")
    return "Async success!"

# Create async retry executor
executor = AsyncRetryExecutor(
    timeout_strategy=LinearTimeStrategy(30, 5),  # Timeout increases linearly
    delay_strategy=ConstantTimeStrategy(1)       # 1 second delay between retries
)

# Execute async operation with retry
try:
    result = await executor.execute(async_operation, max_tries=3)
    print(f"Result: {result}")
except Exception as e:
    print(f"All retry attempts failed: {e}")
```

## Real-World Examples

### Database Connection Retry

```python
from danielutils.retry_executor import RetryExecutor
from danielutils.retry_executor.backoff_strategies import ExponentialBackOffStrategy

def connect_to_database():
    # Simulate database connection
    import random
    if random.random() < 0.5:
        raise ConnectionError("Database connection failed")
    return {"connection": "established"}

# Use exponential backoff for database connections
db_executor = RetryExecutor(ExponentialBackOffStrategy(500))  # Start with 0.5s

def get_database_connection():
    result = db_executor.execute(connect_to_database, max_retries=5)
    if result:
        return result
    raise RuntimeError("Failed to connect to database after all retries")
```

### API Rate Limiting

```python
from danielutils.retry_executor import RetryExecutor
from danielutils.retry_executor.backoff_strategies import LinerBackoffStrategy

def call_external_api():
    import random
    if random.random() < 0.3:
        raise ValueError("Rate limit exceeded")
    return {"data": "API response"}

# Use linear backoff for rate limiting scenarios
api_executor = RetryExecutor(LinerBackoffStrategy(1000, 2000))  # 1s, 3s, 5s, 7s...

def fetch_api_data():
    result = api_executor.execute(call_external_api, max_retries=4)
    return result or {"error": "API unavailable"}
```

### File Operation Retry

```python
from danielutils.retry_executor import RetryExecutor
from danielutils.retry_executor.backoff_strategies import ConstantBackOffStrategy

def read_file_safely():
    try:
        with open("important_file.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError("File not accessible")

# Use constant backoff for file operations
file_executor = RetryExecutor(ConstantBackOffStrategy(500))  # 0.5s delay

def get_file_content():
    result = file_executor.execute(read_file_safely, max_retries=3)
    if result:
        return result
    raise FileNotFoundError("File could not be read after multiple attempts")
```

## Best Practices

1. **Choose Appropriate Backoff Strategy**:
   - Use exponential backoff for network operations
   - Use linear backoff for rate-limited APIs
   - Use constant backoff for file operations
   - Use no backoff for CPU-intensive operations

2. **Set Reasonable Retry Limits**:
   - Don't retry indefinitely
   - Consider the operation's criticality
   - Account for user experience

3. **Handle Exceptions Properly**:
   - Use exception callbacks for logging
   - Distinguish between transient and permanent failures
   - Provide meaningful error messages

4. **Monitor Retry Patterns**:
   - Log retry attempts for debugging
   - Track success rates
   - Adjust strategies based on observed patterns

## Performance Considerations

- **Memory Usage**: Retry executors are lightweight and don't store large amounts of data
- **CPU Overhead**: Minimal overhead, mainly from sleep operations
- **Network Impact**: Exponential backoff helps prevent overwhelming remote services
- **User Experience**: Consider showing progress indicators for long-running retry operations

The Retry Executor provides a robust foundation for building resilient applications that can handle transient failures gracefully. 