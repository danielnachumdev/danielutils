import json
from typing import Callable, Optional, Any, Dict
from pathlib import Path
from datetime import datetime
from .in_memory_database import InMemoryDatabase
from ..database_exceptions import DBException
from ..database_definitions import TableSchema, ColumnType, UpdateQuery, DeleteQuery


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return {
                "__type__": "datetime",
                "value": obj.isoformat()
            }
        return super().default(obj)


class DateTimeDecoder(json.JSONDecoder):
    """Custom JSON decoder for datetime objects"""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(object_hook=self._object_hook, *args, **kwargs)

    def _object_hook(self, obj: dict) -> Any:
        if "__type__" in obj and obj["__type__"] == "datetime":
            return datetime.fromisoformat(obj["value"])
        return obj


class PersistentInMemoryDatabase(InMemoryDatabase):
    """In-memory database with persistence to disk"""

    def __init__(
            self,
            data_dir: str,
            *args,
            auto_save: bool = False,
            register_shutdown_handler: Optional[Callable[[
                Callable[[], None]], None]] = None,
            **kwargs
    ):
        """
        Initialize persistent in-memory database

        Args:
            data_dir (str): Directory to store database files
            auto_save (bool): Whether to save state after every change (default: False)
            register_shutdown_handler (Callable[[Callable[[], None]], None], optional): 
                Function to register shutdown handler. If provided, will be called with a function
                that saves the database state.
        """
        super().__init__()
        self.data_dir = Path(data_dir).resolve()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.auto_save = auto_save

        # Register shutdown handler if provided
        if register_shutdown_handler is not None:
            register_shutdown_handler(self._save_state)

    def _get_state_file(self) -> Path:
        """Get the path to the state file"""
        return self.data_dir / "db_state.json"

    def _save_state(self) -> None:
        """Save current database state to disk"""
        try:
            def filter_callable_defaults(schema_dict):
                # Remove callables from column defaults
                if 'columns' in schema_dict:
                    for col in schema_dict['columns']:
                        if isinstance(col.get('default'), (type(lambda: 0), type(filter_callable_defaults))):
                            col['default'] = None
                        elif callable(col.get('default')):
                            col['default'] = None
                return schema_dict

            state = {
                'tables': self.tables,
                'schemas': {
                    name: filter_callable_defaults(schema.model_dump())
                    for name, schema in self.schemas.items()
                },
                'auto_increment_counters': self.auto_increment_counters
            }
            with open(self._get_state_file(), 'w') as f:
                json.dump(state, f, indent=2, cls=DateTimeEncoder)
            self.logger.info("Database state saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving database state: {e}")
            raise DBException(f"Failed to save database state: {str(e)}", e)

    def _load_state(self) -> None:
        """Load database state from disk if available"""
        state_file = self._get_state_file()
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f, cls=DateTimeDecoder)
                self.tables = state['tables']
                # Convert schema dictionaries back to TableSchema objects
                self.schemas = {
                    name: TableSchema.model_validate(schema_dict)
                    for name, schema_dict in state['schemas'].items()
                }
                # Load auto-increment counters
                self.auto_increment_counters = state.get(
                    'auto_increment_counters', {})

                # If auto_increment_counters is not in the state (old format),
                # initialize it from the existing data
                if not self.auto_increment_counters:
                    self.auto_increment_counters = {}
                    for table_name, schema in self.schemas.items():
                        self.auto_increment_counters[table_name] = {}
                        for column in schema.columns:
                            if column.type == ColumnType.AUTOINCREMENT:
                                # Find the highest value for this column
                                max_id = 0
                                for row in self.tables[table_name].values():
                                    if column.name in row:
                                        max_id = max(max_id, row[column.name])
                                self.auto_increment_counters[table_name][column.name] = max_id

                self.logger.info("Database state loaded successfully")
            except Exception as e:
                self.logger.error(f"Error loading database state: {e}")
                raise DBException(
                    f"Failed to load database state: {str(e)}", e)

    def _maybe_save_state(self) -> None:
        """Save state if auto_save is enabled"""
        if self.auto_save:
            self._save_state()

    def connect(self) -> None:
        """Connect to the database and load state from disk"""
        super().connect()
        self._load_state()

    def disconnect(self) -> None:
        """Close the database connection and save state"""
        self._save_state()
        super().disconnect()

    def create_table(self, schema: TableSchema) -> None:
        """Create a new table with the given schema"""
        super().create_table(schema)
        self._maybe_save_state()

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert a new record into the table"""
        result = super().insert(table, data)
        self._maybe_save_state()
        return result

    def update(self, query: UpdateQuery) -> int:
        """Update records in the table"""
        result = super().update(query)
        self._maybe_save_state()
        return result

    def delete(self, query: DeleteQuery) -> int:
        """Delete records from the table"""
        result = super().delete(query)
        self._maybe_save_state()
        return result


__all__ = [
    "PersistentInMemoryDatabase"
]
