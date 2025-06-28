# Progress Bar System

The Progress Bar System provides advanced progress tracking capabilities with support for multiple concurrent progress bars, custom formatting, and real-time updates. It's designed for both simple single-bar scenarios and complex multi-bar operations.

## Features

- **Multiple Progress Bars**: Display and manage multiple progress bars simultaneously
- **Progress Bar Pools**: Coordinate multiple bars with synchronized updates
- **ASCII Progress Bars**: Terminal-based progress bars with custom formatting
- **Real-time Updates**: Live progress updates with rate calculations
- **Custom Formatting**: Flexible bar format customization
- **Context Manager Support**: Clean resource management with `with` statements
- **Message Integration**: Write messages alongside progress bars

## Basic Usage

### Single Progress Bar

```python
from danielutils.progress_bar import AsciiProgressBar
import time

# Simple progress bar
with AsciiProgressBar(range(100), position=0, desc="Processing") as pbar:
    for i in pbar:
        # Simulate work
        time.sleep(0.01)
        # Progress bar automatically updates
```

### Manual Progress Updates

```python
from danielutils.progress_bar import AsciiProgressBar

# Create progress bar with manual control
pbar = AsciiProgressBar(range(50), position=0, desc="Manual Updates", total=50)

# Update progress manually
pbar.update(10)  # Update by 10 units
pbar.write("Processing batch 1...")  # Write a message
pbar.update(15)  # Update by 15 more units
pbar.write("Processing batch 2...")
pbar.update(25)  # Complete the progress

# Clean up
pbar.reset()
```

## Progress Bar Pools

### Multiple Concurrent Bars

```python
from danielutils.progress_bar import ProgressBarPool, AsciiProgressBar

# Create a pool with 3 progress bars
with ProgressBarPool(AsciiProgressBar, num_of_bars=3) as pool:
    # Configure individual bars
    pool[0].update(30, desc="Downloading")
    pool[1].update(45, desc="Processing")
    pool[2].update(20, desc="Uploading")
    
    # Write a message that appears above all bars
    pool.write("Starting batch processing...")
    
    # Update bars individually
    for i in range(10):
        pool[0].update(1)
        pool[1].update(2)
        pool[2].update(1)
        time.sleep(0.1)
```

### Custom Pool Configuration

```python
from danielutils.progress_bar import ProgressBarPool, AsciiProgressBar

# Global options for all bars
global_options = {
    "ncols": 60,  # Bar width
    "leave": True  # Keep bars after completion
}

# Individual options for each bar
individual_options = [
    {"desc": "Download", "total": 100},
    {"desc": "Process", "total": 50},
    {"desc": "Upload", "total": 75}
]

# Create pool with custom configuration
with ProgressBarPool(
    AsciiProgressBar, 
    num_of_bars=3,
    global_options=global_options,
    individual_options=individual_options
) as pool:
    
    # Update bars with different rates
    for i in range(50):
        pool[0].update(2)  # Download progresses faster
        pool[1].update(1)  # Process at normal rate
        pool[2].update(1.5)  # Upload at medium rate
        time.sleep(0.05)
```

## Advanced Features

### Custom Bar Formatting

```python
from danielutils.progress_bar import AsciiProgressBar

# Custom format with percentage, elapsed time, and rate
custom_format = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt:.2f}{unit}/s]"

pbar = AsciiProgressBar(
    range(100), 
    position=0, 
    desc="Custom Format",
    bar_format=custom_format,
    ncols=40
)

for i in pbar:
    time.sleep(0.02)
```

### Iterating with Progress Bars

```python
from danielutils.progress_bar import AsciiProgressBar

# Process items with progress tracking
items = ["item1", "item2", "item3", "item4", "item5"]

with AsciiProgressBar(items, position=0, desc="Processing Items") as pbar:
    for item in pbar:
        # Process each item
        result = process_item(item)
        pbar.write(f"Processed {item}: {result}")
        time.sleep(0.1)
```

### Nested Progress Bars

```python
from danielutils.progress_bar import ProgressBarPool, AsciiProgressBar

def process_batch(batch_id: int, pool: ProgressBarPool, bar_index: int):
    """Process a batch of items with progress tracking"""
    items = range(20)
    
    for i, item in enumerate(items):
        # Simulate work
        time.sleep(0.05)
        
        # Update the specific bar in the pool
        pool[bar_index].update(1)
        
        # Write status messages
        if i % 5 == 0:
            pool.write(f"Batch {batch_id}: Processed {i+1}/{len(items)} items")

# Process multiple batches concurrently
with ProgressBarPool(AsciiProgressBar, num_of_bars=3) as pool:
    # Configure bar descriptions
    pool[0].desc = "Batch 1"
    pool[1].desc = "Batch 2" 
    pool[2].desc = "Batch 3"
    
    # Process batches
    process_batch(1, pool, 0)
    process_batch(2, pool, 1)
    process_batch(3, pool, 2)
```

## Real-World Examples

### File Processing Pipeline

```python
from danielutils.progress_bar import ProgressBarPool, AsciiProgressBar
import os

def process_files(file_list):
    """Process a list of files with progress tracking"""
    
    with ProgressBarPool(AsciiProgressBar, num_of_bars=3) as pool:
        # Configure bars for different stages
        pool[0].desc = "Reading Files"
        pool[1].desc = "Processing Data"
        pool[2].desc = "Writing Results"
        
        total_files = len(file_list)
        pool[0].total = total_files
        pool[1].total = total_files
        pool[2].total = total_files
        
        for i, filename in enumerate(file_list):
            # Stage 1: Read file
            pool[0].update(1)
            pool.write(f"Reading {filename}")
            data = read_file(filename)
            
            # Stage 2: Process data
            pool[1].update(1)
            pool.write(f"Processing {filename}")
            processed_data = process_data(data)
            
            # Stage 3: Write results
            pool[2].update(1)
            pool.write(f"Writing results for {filename}")
            write_results(filename, processed_data)

# Usage
files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]
process_files(files)
```

### Data Processing with Multiple Stages

```python
from danielutils.progress_bar import ProgressBarPool, AsciiProgressBar

def data_processing_pipeline():
    """Multi-stage data processing with progress tracking"""
    
    with ProgressBarPool(AsciiProgressBar, num_of_bars=4) as pool:
        # Configure all bars
        stages = ["Loading", "Cleaning", "Transforming", "Saving"]
        for i, stage in enumerate(stages):
            pool[i].desc = stage
            pool[i].total = 100
        
        # Stage 1: Loading data
        for i in range(100):
            pool[0].update(1)
            if i % 20 == 0:
                pool.write(f"Loading data chunk {i//20 + 1}/5")
            time.sleep(0.01)
        
        # Stage 2: Cleaning data
        for i in range(100):
            pool[1].update(1)
            if i % 25 == 0:
                pool.write(f"Cleaning data batch {i//25 + 1}/4")
            time.sleep(0.005)
        
        # Stage 3: Transforming data
        for i in range(100):
            pool[2].update(1)
            if i % 33 == 0:
                pool.write(f"Transforming data section {i//33 + 1}/3")
            time.sleep(0.008)
        
        # Stage 4: Saving results
        for i in range(100):
            pool[3].update(1)
            if i % 50 == 0:
                pool.write(f"Saving results part {i//50 + 1}/2")
            time.sleep(0.003)
        
        pool.write("Data processing completed successfully!")

# Run the pipeline
data_processing_pipeline()
```

### Network Operations with Progress

```python
from danielutils.progress_bar import ProgressBarPool, AsciiProgressBar

def download_multiple_files(urls):
    """Download multiple files with progress tracking"""
    
    with ProgressBarPool(AsciiProgressBar, num_of_bars=len(urls)) as pool:
        # Configure bars for each download
        for i, url in enumerate(urls):
            pool[i].desc = f"Download {i+1}"
            pool[i].total = 100
        
        # Simulate downloads
        for i, url in enumerate(urls):
            pool.write(f"Starting download: {url}")
            
            # Simulate download progress
            for progress in range(0, 101, 10):
                pool[i].update(10)
                time.sleep(0.1)
            
            pool.write(f"Completed download: {url}")

# Usage
urls = [
    "https://example.com/file1.zip",
    "https://example.com/file2.zip", 
    "https://example.com/file3.zip"
]
download_multiple_files(urls)
```

## Configuration Options

### ProgressBarPool Options

```python
# Global options applied to all bars
global_options = {
    "ncols": 50,        # Bar width
    "leave": True,      # Keep bars after completion
    "unit": "it",       # Unit label
    "bar_format": "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}"
}

# Individual options for each bar
individual_options = [
    {"desc": "Task 1", "total": 100, "ncols": 40},
    {"desc": "Task 2", "total": 50, "ncols": 60},
    {"desc": "Task 3", "total": 75, "ncols": 45}
]
```

### AsciiProgressBar Options

```python
pbar = AsciiProgressBar(
    iterator=range(100),
    position=0,
    total=100,                    # Total number of items
    desc="Description",           # Bar description
    leave=True,                   # Keep bar after completion
    num_bars=1,                   # Number of bars (for pool)
    ncols=50,                     # Bar width
    pool=None,                    # ProgressBarPool instance
    unit="it",                    # Unit label
    bar_format="custom format"    # Custom format string
)
```

## Best Practices

1. **Use Context Managers**: Always use `with` statements for automatic cleanup
2. **Set Appropriate Totals**: Provide accurate total values for better progress estimation
3. **Write Meaningful Messages**: Use `write()` to provide context about current operations
4. **Handle Exceptions**: Wrap progress bar operations in try-catch blocks
5. **Update Regularly**: Update progress frequently for smooth visual feedback
6. **Clean Up Resources**: Ensure bars are properly reset or closed

## Performance Considerations

- **Update Frequency**: Don't update too frequently (avoid updates every iteration for large datasets)
- **Message Frequency**: Limit the number of messages to avoid terminal clutter
- **Memory Usage**: Progress bars are lightweight and don't store large amounts of data
- **Terminal Performance**: Multiple bars may impact terminal rendering performance

The Progress Bar System provides a comprehensive solution for tracking progress in both simple and complex scenarios, making it easy to provide users with clear feedback about ongoing operations. 