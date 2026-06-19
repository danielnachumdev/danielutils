import unittest
import os
import shutil
import tempfile
from datetime import datetime

from danielutils import RetryExecutor

from danielutils.abstractions.db import (
    SQLiteDatabase, TableSchema, TableColumn, ColumnType,
    SelectQuery, UpdateQuery, DeleteQuery,
    WhereClause, Condition, Operator,
    OrderBy, OrderDirection, DBValidationError
)


class TestSQLiteDatabase(unittest.IsolatedAsyncioTestCase):
    """Test suite for SQLite database implementation"""

    async def asyncSetUp(self):
        """Set up test case"""
        # Create a temporary directory for this test
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test.db")

        # Initialize database with the temporary path
        self.db = SQLiteDatabase(db_name=self.db_path)
        await self.db.connect()

        # Create test table schema
        self.user_schema = TableSchema(
            name="user",
            columns=[
                TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
                TableColumn(name="name", type=ColumnType.VARCHAR, nullable=False),
                TableColumn(name="email", type=ColumnType.VARCHAR, unique=True, nullable=False),
                TableColumn(name="age", type=ColumnType.INTEGER),
                TableColumn(name="created_at", type=ColumnType.DATETIME, nullable=False)
            ]
        )

        # Create test table
        await self.db.create_table(self.user_schema)

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
            await self.db.insert("user", user)

    async def asyncTearDown(self):
        """Clean up test case"""
        await self.db.disconnect()
        RetryExecutor().execute(lambda: shutil.rmtree(self.test_dir), max_retries=2)

    async def test_create_table(self):
        """Test table creation"""
        # Create a new table
        schema = TableSchema(
            name="test_table",
            columns=[
                TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
                TableColumn(name="name", type=ColumnType.VARCHAR)
            ]
        )
        await self.db.create_table(schema)

        # Verify table exists
        schemas = await self.db.get_schemas()
        self.assertIn("test_table", schemas)
        self.assertEqual(len(schemas["test_table"].columns), 2)

    async def test_insert(self):
        """Test record insertion"""
        # Insert a new user
        new_user = {
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "age": 35,
            "created_at": datetime.now()
        }
        user_id = await self.db.insert("user", new_user)

        # Verify insertion
        self.assertIsInstance(user_id, int)
        users = await self.db.get(SelectQuery(table="user"))
        self.assertEqual(len(users), 3)  # Original 2 + new user

    async def test_get(self):
        """Test record retrieval"""
        # Test basic select
        users = await self.db.get(SelectQuery(table="user"))
        self.assertEqual(len(users), 2)

        # Test where clause
        query = SelectQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="age", operator=Operator.GT, value=25)
                ]
            )
        )
        users = await self.db.get(query)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["name"], "John Doe")

        # Test order by
        query = SelectQuery(
            table="user",
            order_by=[OrderBy(column="age", direction=OrderDirection.DESC)]
        )
        users = await self.db.get(query)
        self.assertEqual(users[0]["name"], "John Doe")

        # Test limit
        query = SelectQuery(table="user", limit=1)
        users = await self.db.get(query)
        self.assertEqual(len(users), 1)

    async def test_update(self):
        """Test record updates"""
        # Update user age
        query = UpdateQuery(
            table="user",
            data={"age": 31},
            where=WhereClause(
                conditions=[
                    Condition(column="name", operator=Operator.EQ, value="John Doe")
                ]
            )
        )
        affected = await self.db.update(query)
        self.assertEqual(affected, 1)

        # Verify update
        users = await self.db.get(SelectQuery(table="user"))
        updated_user = next(u for u in users if u["name"] == "John Doe")
        self.assertEqual(updated_user["age"], 31)

    async def test_delete(self):
        """Test record deletion"""
        # Delete a user
        query = DeleteQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="name", operator=Operator.EQ, value="Jane Smith")
                ]
            )
        )
        affected = await self.db.delete(query)
        self.assertEqual(affected, 1)

        # Verify deletion
        users = await self.db.get(SelectQuery(table="user"))
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["name"], "John Doe")

    async def test_validation_errors(self):
        """Test validation error handling"""
        # Test unique constraint violation
        with self.assertRaises(DBValidationError):
            await self.db.insert("user", {
                "name": "Duplicate",
                "email": "john@example.com",  # Duplicate email
                "age": 40,
                "created_at": datetime.now()
            })

        # Test null constraint violation
        with self.assertRaises(DBValidationError):
            await self.db.insert("user", {
                "name": "Missing Email",
                "age": 40,
                "created_at": datetime.now()
            })

    async def test_complex_queries(self):
        """Test complex query operations"""
        # Test multiple conditions
        query = SelectQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="age", operator=Operator.GT, value=20),
                    Condition(column="age", operator=Operator.LT, value=30)
                ],
                operator="AND"
            )
        )
        users = await self.db.get(query)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["name"], "Jane Smith")

        # Test OR conditions
        query = SelectQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="name", operator=Operator.EQ, value="John Doe"),
                    Condition(column="name", operator=Operator.EQ, value="Jane Smith")
                ],
                operator="OR"
            )
        )
        users = await self.db.get(query)
        self.assertEqual(len(users), 2)

    async def test_schema_operations(self):
        """Test schema-related operations"""
        # Get all schemas
        schemas = await self.db.get_schemas()
        self.assertIn("user", schemas)

        # Verify schema details
        user_schema = schemas["user"]
        self.assertEqual(len(user_schema.columns), 5)
        self.assertTrue(any(col.name == "id" and col.primary_key for col in user_schema.columns))
        self.assertTrue(any(col.name == "email" and col.unique for col in user_schema.columns))

    async def test_callable_default_value(self):
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
        await self.db.create_table(schema)
        inserted_id = await self.db.insert("default_test", {})  # No 'value' provided
        result = await self.db.get(SelectQuery(table="default_test"))
        self.assertEqual(result[0]["value"], "supplied_default")


if __name__ == '__main__':
    unittest.main()
