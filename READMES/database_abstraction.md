# Database Abstraction Layer

A unified database interface that provides consistent operations across multiple database backends with automatic schema management and Pydantic integration.

## Features

- **Multiple Backends**: In-Memory, Persistent In-Memory, SQLite (via SQLAlchemy), and Redis
- **Schema Management**: Define table schemas with constraints and automatic validation
- **Pydantic Integration**: Automatic conversion between SQLAlchemy models and database schemas
- **Type-Safe Queries**: Structured query objects with validation
- **Context Manager Support**: Automatic connection management
- **Exception Handling**: Standardized exceptions across implementations

## Quick Start

### Basic Usage

```python
from danielutils.abstractions.db import DatabaseFactory, TableSchema, TableColumn, ColumnType
from danielutils.abstractions.db.database_definitions import SelectQuery, WhereClause, Condition, Operator

# Get a database instance (defaults to persistent in-memory)
db = DatabaseFactory.get_database("persistent_memory")

# Define a table schema
user_schema = TableSchema(
    name="users",
    columns=[
        TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
        TableColumn(name="username", type=ColumnType.TEXT, unique=True, nullable=False),
        TableColumn(name="email", type=ColumnType.TEXT, nullable=False),
        TableColumn(name="age", type=ColumnType.INTEGER, nullable=True)
    ]
)

# Use context manager for automatic connection management
with db:
    # Create the table
    db.create_table(user_schema)
    
    # Insert data
    user_id = db.insert("users", {
        "username": "john_doe",
        "email": "john@example.com",
        "age": 30
    })
    
    # Query data
    query = SelectQuery(
        table="users",
        where=WhereClause(
            conditions=[
                Condition(column="age", operator=Operator.GTE, value=25)
            ]
        )
    )
    
    users = db.get(query)
    print(f"Found {len(users)} users aged 25 or older")
```

## Database Implementations

### 1. In-Memory Database

Fast, temporary storage for testing:

```python
from danielutils.abstractions.db import DatabaseFactory

# Get in-memory database
db = DatabaseFactory.get_database("memory")

# Data is lost when the process ends
with db:
    # Your database operations here
    pass
```

### 2. Persistent In-Memory Database

In-memory storage that persists to disk:

```python
from danielutils.abstractions.db import DatabaseFactory

# Get persistent in-memory database (default)
db = DatabaseFactory.get_database("persistent_memory")

# Data persists between application restarts
with db:
    # Your database operations here
    pass
```

### 3. SQLite Database

Full SQLite database with SQLAlchemy backend:

```python
from danielutils.abstractions.db import DatabaseFactory

# Get SQLite database
db = DatabaseFactory.get_database("sqlite", db_kwargs={"db_name": "my_app.db"})

# Full SQLite functionality with file persistence
with db:
    # Your database operations here
    pass
```

### 4. Redis Database

Redis backend for high-performance applications:

```python
from danielutils.abstractions.db import DatabaseFactory

# Get Redis database
db = DatabaseFactory.get_database("redis", db_kwargs={
    "host": "localhost",
    "port": 6379,
    "db": 0
})

# Redis-backed storage
with db:
    # Your database operations here
    pass
```

## Pydantic Integration with Database Initializer

The database initializer automatically converts SQLAlchemy models to database schemas:

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from danielutils.abstractions.db import DatabaseInitializer, DatabaseFactory

# Define your SQLAlchemy models
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)

# Create a custom initializer
class MyDatabaseInitializer(DatabaseInitializer):
    @classmethod
    def get_pydantic_models(cls):
        """Return all your SQLAlchemy models"""
        return [User]  # Add all your models here

# Initialize database with automatic schema creation
db = DatabaseFactory.get_database("sqlite", db_kwargs={"db_name": "app.db"})
initializer = MyDatabaseInitializer()

with db:
    # This will create all tables based on your SQLAlchemy models
    initializer.init_db(db)
    
    # Now you can use the database normally
    user_id = db.insert("users", {
        "username": "john_doe",
        "email": "john@example.com",
        "is_active": True,
        "created_at": "2024-01-15T10:30:00"
    })
```

## Schema Definition

### Table Schema

Define table structures with constraints:

```python
from danielutils.abstractions.db.database_definitions import (
    TableSchema, TableColumn, TableIndex, ColumnType
)

# Define a table schema
product_schema = TableSchema(
    name="products",
    columns=[
        TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
        TableColumn(name="name", type=ColumnType.TEXT, nullable=False),
        TableColumn(name="price", type=ColumnType.FLOAT, nullable=False),
        TableColumn(name="description", type=ColumnType.TEXT, nullable=True),
        TableColumn(name="is_active", type=ColumnType.BOOLEAN, default=True)
    ],
    indexes=[
        TableIndex(name="idx_product_name", columns=["name"]),
        TableIndex(name="idx_product_active", columns=["is_active"])
    ]
)
```

### Supported Column Types

- **Numeric**: `INTEGER`, `AUTOINCREMENT`, `SMALLINT`, `BIGINT`, `FLOAT`, `DOUBLE`, `DECIMAL`
- **Text**: `TEXT`, `VARCHAR`, `CHAR`
- **Date/Time**: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`
- **Other**: `BOOLEAN`, `BLOB`, `JSON`, `UUID`

## Query Building

### Select Queries

Build queries with conditions and ordering:

```python
from danielutils.abstractions.db.database_definitions import (
    SelectQuery, WhereClause, Condition, Operator, OrderBy, OrderDirection
)

# Simple query
simple_query = SelectQuery(
    table="users",
    columns=["id", "username", "email"]
)

# Query with conditions
filtered_query = SelectQuery(
    table="users",
    where=WhereClause(
        conditions=[
            Condition(column="age", operator=Operator.GTE, value=18),
            Condition(column="is_active", operator=Operator.EQ, value=True)
        ],
        operator="AND"
    ),
    order_by=[
        OrderBy(column="username", direction=OrderDirection.ASC)
    ],
    limit=10
)

# Query with IN clause
in_query = SelectQuery(
    table="products",
    where=WhereClause(
        conditions=[
            Condition(
                column="category_id", 
                operator=Operator.IN, 
                values=[1, 2, 3]
            )
        ]
    )
)
```

### Update Queries

Update records with conditions:

```python
from danielutils.abstractions.db.database_definitions import UpdateQuery

update_query = UpdateQuery(
    table="users",
    data={
        "email": "new_email@example.com",
        "is_active": False
    },
    where=WhereClause(
        conditions=[
            Condition(column="id", operator=Operator.EQ, value=user_id)
        ]
    )
)

affected_rows = db.update(update_query)
```

### Delete Queries

Delete records with conditions:

```python
from danielutils.abstractions.db.database_definitions import DeleteQuery

delete_query = DeleteQuery(
    table="users",
    where=WhereClause(
        conditions=[
            Condition(column="is_active", operator=Operator.EQ, value=False)
        ]
    )
)

affected_rows = db.delete(delete_query)
```

## Supported Operators

The database abstraction supports these comparison operators:

- **Equality**: `EQ` (=), `NEQ` (!=)
- **Comparison**: `GT` (>), `GTE` (>=), `LT` (<), `LTE` (<=)
- **Pattern Matching**: `CONTAINS` (case-insensitive), `CONTAINS_CS` (case-sensitive)
- **Set Operations**: `IN`, `NOT_IN`
- **Null Checks**: `IS_NULL`, `IS_NOT_NULL`

**Note**: `LIKE` and `ILIKE` operators are not supported in In-Memory and Redis databases.

## Exception Handling

Standardized exceptions across all implementations:

```python
from danielutils.abstractions.db.database_exceptions import (
    DBException, DBValidationError, DBQueryError, DBConnectionError
)

try:
    with db:
        db.insert("users", {"username": "test"})
except DBValidationError as e:
    print(f"Validation error: {e}")
except DBQueryError as e:
    print(f"Query error: {e}")
except DBConnectionError as e:
    print(f"Connection error: {e}")
except DBException as e:
    print(f"Database error: {e}")
```

## Best Practices

### 1. Use Context Managers

Always use context managers for automatic connection handling:

```python
# Good
with db:
    result = db.get(query)

# Avoid
db.connect()
try:
    result = db.get(query)
finally:
    db.disconnect()
```

### 2. Use Database Initializer for SQLAlchemy Models

For applications with SQLAlchemy models, use the initializer:

```python
class MyDatabaseInitializer(DatabaseInitializer):
    @classmethod
    def get_pydantic_models(cls):
        return [User, Product, Order]  # All your models

# Initialize once at startup
initializer = MyDatabaseInitializer()
with db:
    initializer.init_db(db)
```

### 3. Handle Auto-Increment Columns

Don't provide values for auto-increment columns:

```python
# Good - let the database handle the ID
user_id = db.insert("users", {
    "username": "john",
    "email": "john@example.com"
})

# Avoid - don't specify auto-increment values
user_id = db.insert("users", {
    "id": 1,  # This will cause an error
    "username": "john",
    "email": "john@example.com"
})
```

### 4. Validate Data Types

Ensure data matches column types:

```python
# Good - correct types
db.insert("users", {
    "username": "john",  # TEXT
    "age": 25,          # INTEGER
    "is_active": True   # BOOLEAN
})

# Avoid - incorrect types
db.insert("users", {
    "username": 123,    # Should be string
    "age": "25",        # Should be integer
    "is_active": "yes"  # Should be boolean
})
```

## Limitations

### In-Memory Database
- No persistent storage
- Limited query capabilities (no LIKE/ILIKE)
- No transaction support

### Redis Database
- Limited query capabilities (no LIKE/ILIKE)
- No complex joins
- Data stored as JSON strings

### SQLite Database
- Requires SQLAlchemy dependency
- File-based storage
- Single-writer limitation

## Dependencies

- **Core**: No external dependencies for basic functionality
- **SQLite**: Requires `sqlalchemy` package
- **Redis**: Requires `redis` package
- **Pydantic Integration**: Requires `pydantic` package

This database abstraction provides a consistent interface across different database backends while maintaining the specific capabilities and limitations of each implementation. 