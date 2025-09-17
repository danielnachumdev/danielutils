import logging
from typing import Dict, Any, List, Type, Union, Sequence
from datetime import datetime
from ...logging_.utils import get_logger

try:
    from starlette import status
except ImportError:
    from ....mock_ import MockImportObject

    status = MockImportObject("`starlette` is not installed")  # type:ignore

from ..database import Database, TableSchema
from ..database_definitions import Operator, WhereClause, Condition, SelectQuery, UpdateQuery, DeleteQuery, ColumnType, \
    TableColumn
from ..database_exceptions import DBValidationError, DBQueryError, DBConnectionError, DBException
from danielutils.logging_.utils import get_logger

class InMemoryDatabase(Database):
    """In-memory database implementation using dictionaries"""

    def is_connected(self) -> bool:
        return self._connected

    @classmethod
    def _default_class_exception_conversion(cls, e: Exception) -> Exception:
        """
        Convert in-memory database specific exceptions to standard database exceptions.
        """
        if isinstance(e, ValueError):
            return DBValidationError(f"Validation error: {str(e)}")
        if isinstance(e, RuntimeError):
            return DBQueryError(f"Query error: {str(e)}")
        return DBException(f"Database error: {str(e)}")

    def __init__(self, *args, **kwargs) -> None:
        try:
            import starlette
        except ImportError as e:
            raise ImportError(f"You must install required dependencies for {self.__class__.__name__}") from e
        # table_name -> {id -> row}
        self.tables: Dict[str, Dict[str, Any]] = {}
        self.schemas: Dict[str, TableSchema] = {}  # table_name -> TableSchema
        # table_name -> {column_name -> last_used_id}
        self.auto_increment_counters: Dict[str, Dict[str, int]] = {}
        self._connected = False
        self.logger = get_logger(__name__)

    async def connect(self) -> None:
        """Connect to the database (no-op for in-memory)"""
        self._connected = True
        self.logger.info("Connected to in-memory database")

    async def disconnect(self) -> None:
        """Disconnect from the database (no-op for in-memory)"""
        self._connected = False
        self.logger.info("Disconnected from in-memory database")

    async def create_table(self, schema: TableSchema) -> None:
        """Create a new table with the given schema"""
        if not self.is_connected():
            raise RuntimeError("Not connected to database")

        if schema.name in self.tables:
            raise ValueError(f"Table '{schema.name}' already exists")

        # Store schema
        self.schemas[schema.name] = schema

        # Create table with empty data
        self.tables[schema.name] = {}

        # Initialize auto-increment counters for this table
        self.auto_increment_counters[schema.name] = {}
        for column in schema.columns:
            if column.type == ColumnType.AUTOINCREMENT:
                self.auto_increment_counters[schema.name][column.name] = 0

        self.logger.info(f"Created table '{schema.name}'")

    def _get_next_auto_increment_id(self, table: str, column: str) -> int:
        """Get the next available ID for an auto-increment column"""
        if table not in self.auto_increment_counters:
            raise ValueError(f"Table '{table}' does not exist")
        if column not in self.auto_increment_counters[table]:
            raise ValueError(
                f"Column '{column}' is not an auto-increment column")

        self.auto_increment_counters[table][column] += 1
        return self.auto_increment_counters[table][column]

    def _revert_auto_increment_counters(self, table: str, column: str) -> None:
        """Revert auto-increment counters"""
        if table not in self.auto_increment_counters:
            raise ValueError(f"Table '{table}' does not exist")
        if column not in self.auto_increment_counters[table]:
            raise ValueError(
                f"Column '{column}' is not an auto-increment column")
        self.auto_increment_counters[table][column] -= 1

    async def get_schemas(self) -> Dict[str, TableSchema]:
        """Get all table schemas"""
        if not self.is_connected():
            raise RuntimeError("Not connected to database")

        return {schema.name: schema for schema in self.schemas.values()}

    async def insert(self, table: str, data: Dict[str, Any]) -> Any:
        """Insert a new row into the table"""
        if not self.is_connected():
            raise RuntimeError("Not connected to database")

        if table not in self.tables:
            raise ValueError(f"Table '{table}' does not exist")

        schema = self.schemas[table]
        row_data = data.copy()

        autoincrements = []
        # Handle auto-increment columns
        for column in schema.columns:
            if column.type == ColumnType.AUTOINCREMENT:
                if column.name in data and data[column.name] is not None:
                    raise DBValidationError(
                        f"Cannot specify value for auto-increment column '{column.name}'")
                autoincrements.append(column)
                row_data[column.name] = self._get_next_auto_increment_id(
                    table, column.name)
        # Generalize: handle any column with a callable default
        columns_to_override_with_defualt = filter(
            lambda column: callable(getattr(column, "default")) and getattr(row_data, column.name, None) is None,
            schema.columns
        )
        for column in columns_to_override_with_defualt:
            # IDK why, but even though this function is a supplier (no args) it
            # raises an error if we dont pass some 'ctx' variable. So that's why we pass None
            row_data[column.name] = column.default(None)

        try:
            # Validate data against schema
            for column in schema.columns:
                if not column.nullable and column.name not in row_data:
                    raise DBValidationError(
                        f"Required column '{column.name}' not provided")
                if column.name in row_data and not self._validate_column_type(column, row_data[column.name]):
                    raise DBValidationError(
                        f"Invalid type for column '{column.name}'")

                # Check unique constraints
                if column.unique and column.name in row_data:
                    # Check if value already exists in any row
                    for existing_row in self.tables[table].values():
                        if self._values_equal(column.type, existing_row.get(column.name), row_data[column.name]):
                            raise DBValidationError(
                                f"Duplicate value for unique column '{column.name}'",
                                status_code=status.HTTP_409_CONFLICT)
        except Exception as e:
            for column in autoincrements:
                self._revert_auto_increment_counters(table, column.name)
            raise

        # Add row
        self.tables[table][row_data['id']] = row_data
        self.logger.info(
            f"Inserted row into '{table}' with ID '{row_data['id']}'")
        return row_data['id']

    async def get(self, query: SelectQuery) -> List[Dict[str, Any]]:
        """Get rows from the table matching the query"""
        if not self.is_connected():
            raise DBConnectionError("Not connected to database")

        if query.table not in self.tables:
            raise ValueError(f"Table '{query.table}' does not exist")

        # Get all rows
        rows = list(self.tables[query.table].values())

        # Apply where clause if present
        if query.where:
            column_names = set(
                column.name for column in self.schemas[query.table].columns)
            for condition in query.where.conditions:
                if condition.column not in column_names:
                    raise DBQueryError(
                        f"Condition on invalid column '{condition.column}'")
            rows = [row for row in rows if self._evaluate_where_clause(
                row, query.where)]

        # Apply order by if present
        if query.order_by:
            for order in reversed(query.order_by):
                rows.sort(
                    key=lambda x: x[order.column],
                    reverse=order.direction == "DESC"
                )

        # Apply limit and offset if present
        if query.offset:
            rows = rows[query.offset:]
        if query.limit:
            rows = rows[:query.limit]

        return rows

    async def update(self, query: UpdateQuery) -> int:
        """Update rows in the table matching the query"""
        if not self.is_connected():
            raise RuntimeError("Not connected to database")

        if query.table not in self.tables:
            raise ValueError(f"Table '{query.table}' does not exist")

        # Get schema for validation
        schema = self.schemas[query.table]
        updated_count = 0

        # Update matching rows
        for row_id, row in self.tables[query.table].items():
            if not query.where or self._evaluate_where_clause(row, query.where):
                # Validate new values against schema
                for column_name, value in query.data.items():
                    column = next(
                        (col for col in schema.columns if col.name == column_name), None)
                    if not column:
                        raise ValueError(
                            f"Column '{column_name}' does not exist")
                    if not self._validate_column_type(column, value):
                        raise ValueError(
                            f"Invalid type for column '{column_name}'")

                # Update row
                row.update(query.data)
                updated_count += 1

        self.logger.info(f"Updated '{updated_count}' rows in '{query.table}'")
        return updated_count

    async def delete(self, query: DeleteQuery) -> int:
        """Delete rows from the table matching the query"""
        if not self.is_connected():
            raise RuntimeError("Not connected to database")

        if query.table not in self.tables:
            raise ValueError(f"Table '{query.table}' does not exist")

        # Find rows to delete
        rows_to_delete = []
        for row_id, row in self.tables[query.table].items():
            if not query.where or self._evaluate_where_clause(row, query.where):
                rows_to_delete.append(row_id)

        # Delete rows
        for row_id in rows_to_delete:
            del self.tables[query.table][row_id]

        self.logger.info(
            f"Deleted {len(rows_to_delete)} rows from '{query.table}'")
        return len(rows_to_delete)

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

        expected_type = type_map.get(column.type.value)
        if not expected_type:
            return False

        if isinstance(expected_type, tuple):
            return isinstance(value, expected_type)
        return isinstance(value, expected_type)

    def _is_case_sensitive_type(self, column_type: ColumnType) -> bool:
        """Check if a column type should use case-sensitive comparison"""
        case_sensitive_types = {
            ColumnType.BLOB,
            ColumnType.JSON,
            ColumnType.UUID
        }
        return column_type in case_sensitive_types

    def _values_equal(self, col_type: ColumnType, val1: Any, val2: Any) -> bool:
        """Compare two values based on column type"""
        if val1 is None or val2 is None:
            return val1 is val2

        if self._is_case_sensitive_type(col_type):
            return val1 == val2

        # Case-insensitive comparison for string types
        if isinstance(val1, str) and isinstance(val2, str):
            return val1.lower() == val2.lower()

        return val1 == val2

    def _evaluate_where_clause(self, row: Dict[str, Any], where_clause: WhereClause) -> bool:
        """Evaluate a where clause against a row"""
        results = [self._evaluate_condition(
            row, condition) for condition in where_clause.conditions]
        if where_clause.operator == "AND":
            return all(results)
        return any(results)

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
        elif condition.operator == Operator.LIKE:
            raise DBQueryError(
                "LIKE operator is not supported in InMemoryDatabase. Use CONTAINS or CONTAINS_CS instead.")
        elif condition.operator == Operator.ILIKE:
            raise DBQueryError(
                "ILIKE operator is not supported in InMemoryDatabase. Use CONTAINS or CONTAINS_CS instead.")
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


__all__ = [
    "InMemoryDatabase"
]
