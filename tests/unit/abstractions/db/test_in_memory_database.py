import unittest
from datetime import datetime
from danielutils.abstractions.db import InMemoryDatabase, TableSchema, TableColumn, ColumnType, SelectQuery, \
    UpdateQuery, DeleteQuery, WhereClause, Condition, Operator, OrderBy, OrderDirection, DBException, DBValidationError, \
    DBQueryError, Database, DBConnectionError


class TestInMemoryDatabase(unittest.IsolatedAsyncioTestCase):
    """Test cases for in-memory database"""

    async def asyncSetUp(self):
        """Set up each test case"""
        # Initialize database
        self.db: Database = InMemoryDatabase()
        await self.db.connect()

        # Create test table
        self.users_schema = TableSchema(
            name="user",
            columns=[
                TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True, nullable=False),
                TableColumn(name="name", type=ColumnType.VARCHAR, nullable=False),
                TableColumn(name="age", type=ColumnType.INTEGER, nullable=True),
                TableColumn(name="email", type=ColumnType.VARCHAR, nullable=False, unique=True),
                TableColumn(name="created_at", type=ColumnType.DATETIME, nullable=False)
            ]
        )
        await self.db.create_table(self.users_schema)

        # Insert test data
        self.test_users = [
            {
                "name": "John Doe",
                "age": 30,
                "email": "john@example.com",
                "created_at": datetime.now()
            },
            {
                "name": "Jane Smith",
                "age": 25,
                "email": "jane@example.com",
                "created_at": datetime.now()
            },
            {
                "name": "Bob Johnson",
                "age": 35,
                "email": "bob@example.com",
                "created_at": datetime.now()
            }
        ]
        for user in self.test_users:
            await self.db.insert("user", user)

    async def asyncTearDown(self):
        """Clean up after each test case"""
        await self.db.disconnect()

    async def test_create_table(self):
        """Test table creation"""
        # Verify table exists
        schemas = await self.db.get_schemas()
        self.assertIn("user", schemas)
        schema = schemas["user"]
        self.assertEqual(schema.name, "user")
        self.assertEqual(len(schema.columns), 5)

        # Verify column types
        column_types = {col.name: col.type for col in schema.columns}
        self.assertEqual(column_types["id"], ColumnType.AUTOINCREMENT)
        self.assertEqual(column_types["name"], ColumnType.VARCHAR)
        self.assertEqual(column_types["age"], ColumnType.INTEGER)
        self.assertEqual(column_types["email"], ColumnType.VARCHAR)
        self.assertEqual(column_types["created_at"], ColumnType.DATETIME)

    async def test_insert_and_get(self):
        """Test data insertion and retrieval"""
        # Query all users
        query = SelectQuery(table="user")
        results = await self.db.get(query)
        self.assertEqual(len(results), 3)

        # Verify user data
        user_data = {user["name"]: user for user in results}
        self.assertEqual(user_data["John Doe"]["age"], 30)
        self.assertEqual(user_data["Jane Smith"]["email"], "jane@example.com")

    async def test_query_with_conditions(self):
        """Test querying with conditions"""
        # Query users over 25
        query = SelectQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="age",
                              operator=Operator.GT, value=25)
                ]
            )
        )
        results = await self.db.get(query)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(user["age"] > 25 for user in results))

    async def test_update(self):
        """Test data update"""
        # Update John's age
        update_query = UpdateQuery(
            table="user",
            data={"age": 31},
            where=WhereClause(
                conditions=[
                    Condition(column="name", operator=Operator.EQ,
                              value="John Doe")
                ]
            )
        )
        await self.db.update(update_query)

        # Verify update
        verify_query = SelectQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="name", operator=Operator.EQ,
                              value="John Doe")
                ]
            )
        )
        updated_user = await self.db.get(verify_query)
        self.assertEqual(updated_user[0]["age"], 31)

    async def test_delete(self):
        """Test data deletion"""
        # Delete Bob
        delete_query = DeleteQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="name", operator=Operator.EQ,
                              value="Bob Johnson")
                ]
            )
        )
        await self.db.delete(delete_query)

        # Verify deletion
        all_users = await self.db.get(SelectQuery(table="user"))
        self.assertEqual(len(all_users), 2)
        self.assertTrue(all(user["name"] != "Bob Johnson" for user in all_users))

    async def test_schema_validation(self):
        """Test schema validation"""
        # Test invalid column type
        with self.assertRaises(DBValidationError):
            await self.db.insert("user", {
                "name": "Invalid User",
                "age": "not a number",  # Should be integer
                "email": "invalid@example.com",
                "created_at": datetime.now()
            })

        # Test missing required field
        with self.assertRaises(DBValidationError):
            await self.db.insert("user", {
                "age": 25,
                "email": "missing_name@example.com",
                "created_at": datetime.now()
            })

        # Test duplicate unique field
        with self.assertRaises(DBValidationError):
            await self.db.insert("user", {
                "name": "Duplicate Email",
                "age": 25,
                "email": "john@example.com",  # Already exists
                "created_at": datetime.now()
            })

        # Test unique constraint with different case (should still be considered duplicate)
        with self.assertRaises(DBValidationError):
            await self.db.insert("user", {
                "name": "Case Sensitive",
                "age": 25,
                "email": "JOHN@example.com",  # Same as existing but different case
                "created_at": datetime.now()
            })

        # Test successful insert with unique value
        new_id = self.db.insert("user", {
            "name": "New User",
            "age": 25,
            "email": "new@example.com",  # Unique email
            "created_at": datetime.now()
        })
        self.assertIsNotNone(new_id)

    async def test_complex_queries(self):
        """Test complex query operations"""
        # Test order by
        query = SelectQuery(
            table="user",
            order_by=[OrderBy(column="age", direction=OrderDirection.DESC)]
        )
        results = await self.db.get(query)
        self.assertEqual(results[0]["name"], "Bob Johnson")
        self.assertEqual(results[1]["name"], "John Doe")
        self.assertEqual(results[2]["name"], "Jane Smith")

        # Test limit
        query = SelectQuery(table="user", limit=2)
        results = await self.db.get(query)
        self.assertEqual(len(results), 2)

        # Test multiple conditions
        query = SelectQuery(
            table="user",
            where=WhereClause(
                conditions=[
                    Condition(column="age",
                              operator=Operator.GT, value=25),
                    Condition(column="name",
                              operator=Operator.CONTAINS_CS, value="ohn ")
                ],
                operator="AND"
            )
        )
        results = await self.db.get(query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "John Doe")

    async def test_error_handling(self):
        """Test error handling"""
        # Test invalid table
        with self.assertRaises(DBValidationError):
            await self.db.get(SelectQuery(table="nonexistent_table"))

        # Test invalid query
        with self.assertRaises(DBQueryError):
            await self.db.get(SelectQuery(
                table="user",
                where=WhereClause(
                    conditions=[
                        Condition(column="nonexistent_column", operator=Operator.EQ, value=1)]
                )
            ))

        # Test disconnection
        await self.db.disconnect()
        with self.assertRaises(DBConnectionError):
            await self.db.get(SelectQuery(table="user"))

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
