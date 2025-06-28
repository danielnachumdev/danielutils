# Async Worker Pool

The Async Worker Pool provides a robust system for managing concurrent asynchronous tasks with configurable worker pools, progress tracking, and comprehensive logging. It's designed for scenarios where you need to process multiple async operations efficiently with proper resource management.

## Features

- **Configurable Worker Pools**: Set the number of concurrent workers
- **Task Queue Management**: Automatic task distribution across workers
- **Progress Tracking**: Optional progress bar integration with tqdm
- **Comprehensive Logging**: Detailed logging with structured JSON output
- **Graceful Shutdown**: Proper cleanup and worker termination
- **Task Naming**: Optional task names for better tracking
- **Exception Handling**: Robust error handling and reporting

## Basic Usage

### Simple Worker Pool

```python
import asyncio
from danielutils.async_ import AsyncWorkerPool

async def simple_task(task_id: int):
    """Simple async task that simulates work"""
    await asyncio.sleep(1)  # Simulate async work
    print(f"Task {task_id} completed")

async def main():
    # Create a worker pool with 3 workers
    pool = AsyncWorkerPool("SimplePool", num_workers=3, show_pbar=True)
    
    # Start the pool
    await pool.start()
    
    # Submit tasks
    for i in range(10):
        await pool.submit(simple_task, args=(i,), name=f"task_{i}")
    
    # Wait for all tasks to complete and shutdown workers
    await pool.join()

# Run the example
asyncio.run(main())
```

### Worker Pool with Progress Tracking

```python
import asyncio
from danielutils.async_ import AsyncWorkerPool

async def processing_task(data: str, delay: float = 0.5):
    """Task that processes data with configurable delay"""
    await asyncio.sleep(delay)
    result = f"Processed: {data.upper()}"
    return result

async def main():
    # Create pool with progress bar
    pool = AsyncWorkerPool("DataProcessor", num_workers=4, show_pbar=True)
    
    # Data to process
    data_items = [f"item_{i}" for i in range(20)]
    
    # Start the pool
    await pool.start()
    
    # Submit all tasks
    for item in data_items:
        await pool.submit(
            processing_task, 
            args=(item,), 
            name=f"process_{item}"
        )
    
    # Wait for completion and cleanup
    await pool.join()

asyncio.run(main())
```

## Advanced Usage

### Custom Logging and Error Handling

```python
import asyncio
from danielutils.async_ import AsyncWorkerPool

async def risky_task(task_id: int, should_fail: bool = False):
    """Task that might fail"""
    await asyncio.sleep(0.1)
    
    if should_fail:
        raise ValueError(f"Task {task_id} failed intentionally")
    
    return f"Task {task_id} succeeded"

async def main():
    # Create pool with custom configuration
    pool = AsyncWorkerPool("RiskyTasks", num_workers=2, show_pbar=False)
    
    # Start the pool
    await pool.start()
    
    # Submit mix of successful and failing tasks
    for i in range(10):
        should_fail = i % 3 == 0  # Every 3rd task fails
        await pool.submit(
            risky_task, 
            args=(i, should_fail), 
            name=f"risky_task_{i}"
        )
    
    # Wait for completion and cleanup
    await pool.join()

asyncio.run(main())
```

### Complex Task Processing

```python
import asyncio
from danielutils.async_ import AsyncWorkerPool
import random

async def data_processing_pipeline(data: dict):
    """Complex data processing task"""
    # Stage 1: Validation
    await asyncio.sleep(0.1)
    if not data.get("valid", True):
        raise ValueError("Invalid data")
    
    # Stage 2: Processing
    await asyncio.sleep(0.2)
    processed_data = {
        "id": data["id"],
        "processed_value": data["value"] * 2,
        "timestamp": asyncio.get_event_loop().time()
    }
    
    # Stage 3: Storage simulation
    await asyncio.sleep(0.1)
    if random.random() < 0.1:  # 10% chance of storage failure
        raise RuntimeError("Storage error")
    
    return processed_data

async def main():
    # Create worker pool
    pool = AsyncWorkerPool("DataPipeline", num_workers=3, show_pbar=True)
    
    # Generate test data
    test_data = [
        {"id": i, "value": i * 10, "valid": True}
        for i in range(50)
    ]
    
    # Add some invalid data
    test_data.extend([
        {"id": 100, "value": 1000, "valid": False},
        {"id": 101, "value": 2000, "valid": False}
    ])
    
    # Start pool
    await pool.start()
    
    # Submit processing tasks
    for data in test_data:
        await pool.submit(
            data_processing_pipeline,
            args=(data,),
            name=f"process_data_{data['id']}"
        )
    
    # Wait for completion and cleanup
    await pool.join()

asyncio.run(main())
```

## Real-World Examples

### Web Scraping with Rate Limiting

```python
import asyncio
import aiohttp
from danielutils.async_ import AsyncWorkerPool

async def scrape_url(session: aiohttp.ClientSession, url: str):
    """Scrape a single URL with rate limiting"""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                return {
                    "url": url,
                    "status": "success",
                    "length": len(content)
                }
            else:
                return {
                    "url": url,
                    "status": "error",
                    "error": f"HTTP {response.status}"
                }
    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }

async def main():
    # URLs to scrape
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/404",
        "https://httpbin.org/status/500",
        "https://invalid-url-that-will-fail.com"
    ]
    
    # Create worker pool
    pool = AsyncWorkerPool("WebScraper", num_workers=3, show_pbar=True)
    
    # Start pool
    await pool.start()
    
    # Create session for all workers to share
    async with aiohttp.ClientSession() as session:
        # Submit scraping tasks
        for url in urls:
            await pool.submit(
                scrape_url,
                args=(session, url),
                name=f"scrape_{url.split('/')[-1]}"
            )
        
        # Wait for completion and cleanup
        await pool.join()

asyncio.run(main())
```

### Database Operations

```python
import asyncio
from danielutils.async_ import AsyncWorkerPool
import sqlite3
import threading

# Thread-local storage for database connections
thread_local = threading.local()

def get_db_connection():
    """Get or create database connection for current thread"""
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = sqlite3.connect(':memory:')
        # Create table
        thread_local.connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
    return thread_local.connection

async def insert_user(user_data: dict):
    """Insert a user into the database"""
    # Run database operation in thread pool
    loop = asyncio.get_event_loop()
    
    def db_operation():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user_data['name'], user_data['email'])
        )
        conn.commit()
        return cursor.lastrowid
    
    user_id = await loop.run_in_executor(None, db_operation)
    return {"user_id": user_id, "name": user_data['name']}

async def main():
    # Sample user data
    users = [
        {"name": f"User_{i}", "email": f"user{i}@example.com"}
        for i in range(100)
    ]
    
    # Create worker pool
    pool = AsyncWorkerPool("DatabaseOps", num_workers=4, show_pbar=True)
    
    # Start pool
    await pool.start()
    
    # Submit database operations
    for user in users:
        await pool.submit(
            insert_user,
            args=(user,),
            name=f"insert_user_{user['name']}"
        )
    
    # Wait for completion and cleanup
    await pool.join()
    
    # Verify results
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"Inserted {count} users")

asyncio.run(main())
```

### File Processing Pipeline

```python
import asyncio
import os
from danielutils.async_ import AsyncWorkerPool

async def process_file(filepath: str):
    """Process a single file"""
    try:
        # Simulate file processing
        await asyncio.sleep(0.1)
        
        # Get file info
        stat = os.stat(filepath)
        
        # Simulate processing based on file size
        if stat.st_size > 1000:
            await asyncio.sleep(0.2)  # Larger files take longer
        
        return {
            "filepath": filepath,
            "size": stat.st_size,
            "status": "processed"
        }
    except Exception as e:
        return {
            "filepath": filepath,
            "status": "error",
            "error": str(e)
        }

async def main():
    # Create some test files
    test_files = []
    for i in range(20):
        filename = f"test_file_{i}.txt"
        with open(filename, 'w') as f:
            f.write("x" * (i * 100))  # Files of different sizes
        test_files.append(filename)
    
    try:
        # Create worker pool
        pool = AsyncWorkerPool("FileProcessor", num_workers=3, show_pbar=True)
        
        # Start pool
        await pool.start()
        
        # Submit file processing tasks
        for filepath in test_files:
            await pool.submit(
                process_file,
                args=(filepath,),
                name=f"process_{os.path.basename(filepath)}"
            )
        
        # Wait for completion and cleanup
        await pool.join()
        
    finally:
        # Clean up test files
        for filepath in test_files:
            try:
                os.remove(filepath)
            except:
                pass

asyncio.run(main())
```

## Configuration Options

### AsyncWorkerPool Parameters

```python
pool = AsyncWorkerPool(
    pool_name="MyPool",           # Name for logging and identification
    num_workers=5,                # Number of concurrent workers
    show_pbar=True               # Enable progress bar (requires tqdm)
)
```

### Task Submission Options

```python
await pool.submit(
    func,                        # Async function to execute
    args=(arg1, arg2),           # Positional arguments
    kwargs={"key": "value"},     # Keyword arguments
    name="task_name"             # Optional task name for logging
)
```

## Logging and Monitoring

The AsyncWorkerPool provides comprehensive logging with structured JSON output:

```python
# Example log output:
{
    "pool": "MyPool",
    "timestamp": "2024-01-15T10:30:45.123456",
    "worker_id": 1,
    "task_id": 5,
    "task_name": "process_data_123",
    "level": "INFO",
    "message": "Started"
}
```

## Best Practices

1. **Worker Count**: Choose worker count based on I/O vs CPU-bound tasks
2. **Resource Management**: Ensure proper cleanup of resources (connections, files)
3. **Error Handling**: Design tasks to handle exceptions gracefully
4. **Task Naming**: Use descriptive task names for better monitoring
5. **Graceful Shutdown**: Always use `pool.join()` for proper cleanup

## Performance Considerations

- **Memory Usage**: Each worker maintains its own task context
- **CPU Overhead**: Minimal overhead for task distribution
- **I/O Efficiency**: Excellent for I/O-bound operations
- **Scalability**: Worker count can be adjusted based on system resources

## Limitations

- **Task Dependencies**: No built-in support for task dependencies
- **Result Collection**: Results are not automatically collected
- **Priority Queues**: No priority-based task scheduling
- **Persistent Queues**: Tasks are not persisted across restarts

The Async Worker Pool provides a robust foundation for managing concurrent async operations with proper resource management and comprehensive monitoring capabilities. 