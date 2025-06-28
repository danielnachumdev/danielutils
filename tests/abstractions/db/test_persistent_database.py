import unittest
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import cast

from danielutils.abstractions.db import PersistentInMemoryDatabase, TableSchema, TableColumn, ColumnType, SelectQuery, UpdateQuery, \
    DeleteQuery, WhereClause, Condition, Operator, Database


class TestPersistentDatabase(unittest.TestCase):
    """Test cases for persistent in-memory database"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Set up test data directory
        cls.test_dir = Path("./test_data").resolve()
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)
        cls.test_dir.mkdir()

    def setUp(self):
        """Set up each test case"""
        # Initialize database
        self.db: Database = PersistentInMemoryDatabase(
            data_dir=str(self.test_dir),
            register_shutdown_handler=lambda handler: None
        )
        self.db.connect()

        # Create test table schema
        self.user_schema = TableSchema(
            name="user",
            columns=[
                TableColumn(name="id", type=ColumnType.AUTOINCREMENT,
                            primary_key=True, nullable=False),
                TableColumn(name="name", type=ColumnType.VARCHAR,
                            nullable=False),
                TableColumn(name="email", type=ColumnType.VARCHAR,
                            nullable=False, unique=True),
                TableColumn(name="age", type=ColumnType.INTEGER,
                            nullable=True),
                TableColumn(name="created_at",
                            type=ColumnType.DATETIME, nullable=False)
            ]
        )

        # Create table
        self.db.create_table(self.user_schema)

        # Insert test data
        self.test_users = [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30,
                "created_at": datetime.now()
            },
            {
                "name": "Jane Smith",
                "email": "jane@example.com",
                "age": 25,
                "created_at": datetime.now()
            }
        ]

        for user in self.test_users:
            self.db.insert("user", user)
        cast(PersistentInMemoryDatabase, self.db)._save_state()

    def tearDown(self):
        """Clean up test environment"""
        self.db.disconnect()
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()

    def test_persistence_across_connections(self):
        """Test that data persists across database connections"""
        # Insert some data
        new_user = {
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "age": 35,
            "created_at": datetime.now()
        }
        self.db.insert("user", new_user)

        # Disconnect and reconnect
        self.db.disconnect()
        self.db.connect()

        # Verify data persistence
        query = SelectQuery(table="user")
        users = self.db.get(query)
        self.assertEqual(len(users), 3)

        # Verify specific data
        user_data = {user["email"]: user for user in users}
        self.assertEqual(user_data["bob@example.com"]["name"], "Bob Wilson")
        self.assertEqual(user_data["bob@example.com"]["age"], 35)

    def test_state_file_creation(self):
        """Test that state file is created and contains correct data"""
        # Disconnect to trigger state save
        self.db.disconnect()

        # Check state file exists
        state_file = self.test_dir / "db_state.json"
        self.assertTrue(state_file.exists())

        # Verify state file content
        with open(state_file, 'r') as f:
            state = json.load(f)
        self.assertIn("tables", state)
        self.assertIn("user", state["tables"])
        self.assertEqual(len(state["tables"]["user"]), 2)

        # Verify user data in state file
        user_data = {user["email"]: user for user in state["tables"]["user"].values()}
        self.assertEqual(user_data["john@example.com"]["name"], "John Doe")
        self.assertEqual(user_data["jane@example.com"]["age"], 25)

    def test_schema_persistence(self):
        """Test that schema persists across connections"""
        # Disconnect and reconnect
        self.db.disconnect()
        self.db.connect()

        # Verify schema
        schemas = self.db.get_schemas()
        self.assertIn("user", schemas)
        schema = schemas["user"]
        self.assertEqual(schema.name, "user")
        self.assertEqual(len(schema.columns), 5)

        # Verify column types and constraints
        column_types = {col.name: col.type for col in schema.columns}
        self.assertEqual(column_types["id"], ColumnType.AUTOINCREMENT)
        self.assertEqual(column_types["name"], ColumnType.VARCHAR)
        self.assertEqual(column_types["email"], ColumnType.VARCHAR)

        # Verify constraints
        email_column = next(
            col for col in schema.columns if col.name == "email")
        self.assertTrue(email_column.unique)
        self.assertFalse(email_column.nullable)

    def test_data_integrity_after_reload(self):
        """Test that data integrity is maintained after reloading"""
        # Perform some operations
        update_query = UpdateQuery(
            table="user",
            data={"age": 31},
            where=WhereClause(
                conditions=[
                    Condition(column="email", operator=Operator.EQ,
                              value="john@example.com")
                ]
            )
        )
        self.db.update(update_query)

        delete_query = DeleteQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="email", operator=Operator.EQ,
                              value="jane@example.com")
                ]
            )
        )
        self.db.delete(delete_query)

        # Disconnect and reconnect
        self.db.disconnect()
        self.db.connect()

        # Verify data integrity
        query = SelectQuery(table="user")
        users = self.db.get(query)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["email"], "john@example.com")
        self.assertEqual(users[0]["age"], 31)

    def test_shutdown_handler(self):
        """Test that shutdown handler is registered with atexit"""
        # Track registered handlers
        registered_handlers = []

        def register_handler(handler):
            # Simulate atexit.register by storing the handler
            registered_handlers.append(handler)

        # Create new instance with handler registration
        db = PersistentInMemoryDatabase(
            data_dir=str(self.test_dir),
            register_shutdown_handler=register_handler
        )
        db.connect()

        # Insert some data to verify it's saved
        db.insert("user", {
            "name": "Test User",
            "email": "test@example.com",
            "age": 25,
            "created_at": datetime.now()
        })

        # Verify handler was registered
        self.assertEqual(len(registered_handlers), 1)
        shutdown_handler = registered_handlers[0]

        # Simulate application exit by calling the registered handler
        shutdown_handler()

        # Verify data was saved by creating a new instance and checking
        new_db = PersistentInMemoryDatabase(data_dir=str(self.test_dir))
        new_db.connect()
        users = new_db.get(SelectQuery(table="user"))
        self.assertEqual(len(users), 3)  # Original 2 + our new test user
        new_db.disconnect()

    def test_callable_default_value(self):
        """Test that callable default value suppliers are used when value is missing"""
        def default_supplier(ctx):
            return "supplied_default"
        schema = TableSchema(
            name="default_test",
            columns=[
                TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
                TableColumn(name="value", type=ColumnType.VARCHAR, default=default_supplier)
            ]
        )
        self.db.create_table(schema)
        inserted_id = self.db.insert("default_test", {})  # No 'value' provided
        result = self.db.get(SelectQuery(table="default_test"))
        self.assertEqual(result[0]["value"], "supplied_default")


if __name__ == '__main__':
    unittest.main()
