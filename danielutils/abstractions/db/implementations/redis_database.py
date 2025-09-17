import json
import logging
from typing import List, Dict, Any, Optional, Type, Union, Sequence
from datetime import datetime
from ....logging_.utils import get_logger

try:
    import redis.asyncio as redis
except ImportError:
    from ....mock_ import MockImportObject

    redis = MockImportObject("`redis` is not installed")  # type:ignore

from ..database import Database
from ..database_definitions import (
    DeleteQuery, UpdateQuery, SelectQuery, TableSchema,
    Operator, WhereClause, Condition, ColumnType, TableColumn
)
from ..database_exceptions import DBException, DBValidationError, DBQueryError, DBConnectionError

class RedisDatabase(Database):
    """Redis implementation of the Database abstract class"""

    @classmethod
    def _default_class_exception_conversion(cls, e: Exception) -> Exception:
        """
        Convert Redis-specific exceptions to standard database exceptions.
        """
        if isinstance(e, redis.ConnectionError):
            return DBConnectionError(f"Redis connection error: {str(e)}")
        elif isinstance(e, redis.RedisError):
            return DBException(f"Redis error: {str(e)}")
        elif isinstance(e, ValueError):
            return DBValidationError(f"Validation error: {str(e)}")
        elif isinstance(e, RuntimeError):
            return DBQueryError(f"Query error: {str(e)}")
        return DBException(f"Database error: {str(e)}")

    def __init__(self, host='localhost', port=6379, db=0, password=None, decode_responses=True) -> None:
        """
        Initialize Redis database connection

        Args:
            host (str): Redis host
            port (int): Redis port
            db (int): Redis database number
            password (str, optional): Redis password
            decode_responses (bool): Whether to decode responses to strings
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self._db: redis.Redis = None  # type:ignore
        self._connected = False
        self.logger = get_logger(__name__)

        # Redis key prefixes
        self.SCHEMA_PREFIX = "schema:"
        self.TABLE_PREFIX = "table:"
        self.COUNTER_PREFIX = "counter:"

    def is_connected(self) -> bool:
        return self._connected

    async def connect(self) -> None:
        """Establish connection to Redis database"""
        try:
            self._db = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=self.decode_responses
            )
            # Test connection
            await self._db.ping()
            self._connected = True
            self.logger.info(
                f"Connected to Redis database at {self.host}:{self.port}")
        except Exception as e:
            self.logger.error(f"Error connecting to Redis database: {e}")
            raise

    async def disconnect(self) -> None:
        """Close the Redis database connection"""
        if self._db:
            await self._db.aclose()
            self._connected = False
            self.logger.info("Disconnected from Redis database")

    def _assert_connection(self) -> None:
        """Check if connected to database"""
        if not self._connected or not self._db:
            raise DBConnectionError("Not connected to database")

    async def get_schemas(self) -> Dict[str, TableSchema]:
        """Get all table schemas"""
        self._assert_connection()

        schemas = {}
        # Get all schema keys
        schema_keys = await self._db.keys(f"{self.SCHEMA_PREFIX}*")

        for key in schema_keys:
            table_name = key[len(self.SCHEMA_PREFIX):]
            schema_json = await self._db.get(key)
            if schema_json:
                schema_dict = json.loads(schema_json)
                schemas[table_name] = TableSchema.model_validate(schema_dict)

        return schemas

    async def create_table(self, schema: TableSchema) -> None:
        """Create a new table with the given schema"""
        self._assert_connection()

        schema_key = f"{self.SCHEMA_PREFIX}{schema.name}"
        if await self._db.exists(schema_key):
            raise ValueError(f"Table '{schema.name}' already exists")

        # Store schema as JSON
        schema_json = schema.to_json()
        await self._db.set(schema_key, schema_json)

        # Initialize auto-increment counters
        for column in schema.columns:
            if column.type == ColumnType.AUTOINCREMENT:
                counter_key = f"{self.COUNTER_PREFIX}{schema.name}:{column.name}"
                await self._db.set(counter_key, 0)

        self.logger.info(f"Created table '{schema.name}'")

    async def _get_next_auto_increment_id(self, table: str, column: str) -> int:
        """Get the next available ID for an auto-increment column"""
        counter_key = f"{self.COUNTER_PREFIX}{table}:{column}"
        return await self._db.incr(counter_key)

    def _validate_column_type(self, column: TableColumn, value: Any) -> bool:
        """Validate a value against a column's type"""
        if value is None:
            return column.nullable

        type_map: Dict[str, Union[Type, Sequence[Type]]] = {
            "INTEGER": int,
            "BIGINT": int,
            "FLOAT": float,
            "DOUBLE": float,
            "DECIMAL": float,
            "BOOLEAN": bool,
            "TEXT": str,
            "VARCHAR": str,
            "CHAR": str,
            "DATE": (str, datetime),
            "TIME": (str, datetime),
            "DATETIME": (str, datetime),
            "TIMESTAMP": (str, datetime),
            "BLOB": bytes,
            "JSON": (dict, list),
            "UUID": str,
            "AUTOINCREMENT": int
        }

        expected_type = type_map.get(column.type.value, None)
        if not expected_type:
            return False

        if isinstance(expected_type, tuple):
            return isinstance(value, expected_type)
        return isinstance(value, expected_type)  # type: ignore

    async def insert(self, table: str, data: Dict[str, Any]) -> Any:
        """Insert a new record into the specified table"""
        self._assert_connection()

        # Get schema
        schema_key = f"{self.SCHEMA_PREFIX}{table}"
        schema_json = await self._db.get(schema_key)
        if not schema_json:
            raise ValueError(f"Table '{table}' does not exist")

        schema = TableSchema.model_validate(json.loads(schema_json))
        row_data = data.copy()

        # Handle auto-increment columns
        for column in schema.columns:
            if column.type == ColumnType.AUTOINCREMENT:
                if column.name in data and data[column.name] is not None:
                    raise DBValidationError(f"Cannot specify value for auto-increment column '{column.name}'")
                row_data[column.name] = await self._get_next_auto_increment_id(table, column.name)

        # Validate data against schema
        for column in schema.columns:
            if column.name in row_data:
                if not self._validate_column_type(column, row_data[column.name]):
                    raise DBValidationError(f"Invalid type for column '{column.name}'")
            elif not column.nullable and column.default is None:
                raise DBValidationError(f"Required column '{column.name}' has no value")

        # Generate unique ID for the row
        row_id = str(await self._get_next_auto_increment_id(table, "_id"))

        # Store row data as hash
        table_key = f"{self.TABLE_PREFIX}{table}"
        row_key = f"{row_id}"

        # Convert data to strings for Redis hash
        hash_data = {}
        for key, value in row_data.items():
            if isinstance(value, (dict, list)):
                hash_data[key] = json.dumps(value)
            else:
                hash_data[key] = str(value)

        await self._db.hset(table_key, row_key, json.dumps(hash_data))  # type: ignore

        self.logger.info(f"Inserted row {row_id} into table '{table}'")
        return row_id

    def _evaluate_condition(self, row: Dict[str, Any], condition: Condition) -> bool:
        """Evaluate a single condition against a row"""
        if condition.column not in row:
            return False

        value = row[condition.column]
        if condition.operator == Operator.EQ:
            return value == condition.value
        elif condition.operator == Operator.NEQ:
            return value != condition.value
        elif condition.operator == Operator.GT:
            return value > condition.value
        elif condition.operator == Operator.GTE:
            return value >= condition.value
        elif condition.operator == Operator.LT:
            return value < condition.value
        elif condition.operator == Operator.LTE:
            return value <= condition.value
        elif condition.operator == Operator.CONTAINS:
            return str(condition.value).lower() in str(value).lower()
        elif condition.operator == Operator.CONTAINS_CS:
            return str(condition.value) in str(value)
        elif condition.operator == Operator.IN:
            return value in condition.values  # type: ignore
        elif condition.operator == Operator.NOT_IN:
            return value not in condition.values  # type: ignore
        elif condition.operator == Operator.IS_NULL:
            return value is None
        elif condition.operator == Operator.IS_NOT_NULL:
            return value is not None
        return False

    def _evaluate_where_clause(self, row: Dict[str, Any], where_clause: WhereClause) -> bool:
        """Evaluate a where clause against a row"""
        results = [self._evaluate_condition(row, condition) for condition in where_clause.conditions]
        if where_clause.operator == "AND":
            return all(results)
        return any(results)

    async def get(self, query: SelectQuery) -> List[Dict[str, Any]]:
        """Get records from the database"""
        self._assert_connection()

        # Get schema
        schema_key = f"{self.SCHEMA_PREFIX}{query.table}"
        schema_json = await self._db.get(schema_key)
        if not schema_json:
            raise ValueError(f"Table '{query.table}' does not exist")

        schema = TableSchema.model_validate(json.loads(schema_json))

        # Get all rows from the table
        table_key = f"{self.TABLE_PREFIX}{query.table}"
        all_rows = await self._db.hgetall(table_key)  # type: ignore

        rows = []
        for row_id, row_json in all_rows.items():
            row_data = json.loads(row_json)

            # Convert string values back to appropriate types
            processed_row = {}
            for col in schema.columns:
                if col.name in row_data:
                    value = row_data[col.name]
                    # Try to convert back to original type
                    if col.type in [ColumnType.INTEGER, ColumnType.BIGINT, ColumnType.AUTOINCREMENT]:
                        try:
                            processed_row[col.name] = int(value)
                        except (ValueError, TypeError):
                            processed_row[col.name] = value
                    elif col.type in [ColumnType.FLOAT, ColumnType.DOUBLE, ColumnType.DECIMAL]:
                        try:
                            processed_row[col.name] = float(value)  # type: ignore
                        except (ValueError, TypeError):
                            processed_row[col.name] = value
                    elif col.type == ColumnType.BOOLEAN:
                        processed_row[col.name] = value.lower() in ('true', '1', 'yes')
                    elif col.type == ColumnType.JSON:
                        try:
                            processed_row[col.name] = json.loads(value)
                        except (ValueError, TypeError):
                            processed_row[col.name] = value
                    else:
                        processed_row[col.name] = value

            rows.append(processed_row)

        # Apply where clause if present
        if query.where:
            column_names = set(column.name for column in schema.columns)
            for condition in query.where.conditions:
                if condition.column not in column_names:
                    raise DBQueryError(f"Condition on invalid column '{condition.column}'")
            rows = [row for row in rows if self._evaluate_where_clause(row, query.where)]

        # Apply order by if present
        if query.order_by:
            for order in reversed(query.order_by):
                rows.sort(key=lambda x: x.get(order.column, ''), reverse=order.direction == "DESC")

        # Apply limit and offset if present
        if query.offset:
            rows = rows[query.offset:]
        if query.limit:
            rows = rows[:query.limit]

        return rows

    async def update(self, query: UpdateQuery) -> int:
        """Update records in the database"""
        self._assert_connection()

        # Get schema
        schema_key = f"{self.SCHEMA_PREFIX}{query.table}"
        schema_json = await self._db.get(schema_key)
        if not schema_json:
            raise ValueError(f"Table '{query.table}' does not exist")

        schema = TableSchema.model_validate(json.loads(schema_json))
        updated_count = 0

        # Get all rows from the table
        table_key = f"{self.TABLE_PREFIX}{query.table}"
        all_rows = await self._db.hgetall(table_key)  # type: ignore

        # Validate new values against schema
        for column_name, value in query.data.items():
            column = next((col for col in schema.columns if col.name == column_name), None)
            if not column:
                raise ValueError(f"Column '{column_name}' does not exist")
            if not self._validate_column_type(column, value):
                raise ValueError(f"Invalid type for column '{column_name}'")

        # Update matching rows
        for row_id, row_json in all_rows.items():
            row_data = json.loads(row_json)

            if not query.where or self._evaluate_where_clause(row_data, query.where):
                # Update row data
                for key, value in query.data.items():
                    if isinstance(value, (dict, list)):
                        row_data[key] = json.dumps(value)
                    else:
                        row_data[key] = str(value)

                # Store updated row
                await self._db.hset(table_key, row_id, json.dumps(row_data))  # type: ignore
                updated_count += 1

        self.logger.info(f"Updated {updated_count} rows in '{query.table}'")
        return updated_count

    async def delete(self, query: DeleteQuery) -> int:
        """Delete records from the database"""
        self._assert_connection()

        # Get schema
        schema_key = f"{self.SCHEMA_PREFIX}{query.table}"
        schema_json = await self._db.get(schema_key)
        if not schema_json:
            raise ValueError(f"Table '{query.table}' does not exist")

        # Get all rows from the table
        table_key = f"{self.TABLE_PREFIX}{query.table}"
        all_rows = await self._db.hgetall(table_key)  # type: ignore

        # Find rows to delete
        rows_to_delete = []
        for row_id, row_json in all_rows.items():
            row_data = json.loads(row_json)
            if not query.where or self._evaluate_where_clause(row_data, query.where):
                rows_to_delete.append(row_id)

        # Delete rows
        for row_id in rows_to_delete:
            await self._db.hdel(table_key, row_id)  # type: ignore

        self.logger.info(f"Deleted {len(rows_to_delete)} rows from '{query.table}'")
        return len(rows_to_delete)


__all__ = [
    "RedisDatabase"
]
