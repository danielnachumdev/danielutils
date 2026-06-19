import asyncio
import unittest
import json

from danielutils import DBConnectionError
from danielutils.abstractions.db.implementations.redis_database import RedisDatabase
from danielutils.abstractions.db.database_definitions import (
    TableSchema, TableColumn, ColumnType, SelectQuery, UpdateQuery, DeleteQuery,
    WhereClause, Condition, Operator
)

import redis.asyncio as redis


class TestRedisDatabase(unittest.IsolatedAsyncioTestCase):
    """Test cases for RedisDatabase implementation (integration with real Redis)"""

    async def asyncSetUp(self):
        # Try to connect to Redis, skip tests if not available
        try:
            self._redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            await self._redis.ping()
        except Exception as e:
            raise unittest.SkipTest(f"Redis server is not available: {e}")
        # Flush DB before each test for isolation
        await self._redis.flushdb()
        self.db = RedisDatabase(host='localhost', port=6379, db=0)
        await self.db.connect()
        self.sample_schema = TableSchema(
            name="users",
            columns=[
                TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
                TableColumn(name="name", type=ColumnType.TEXT, nullable=False),
                TableColumn(name="email", type=ColumnType.TEXT, nullable=False),
                TableColumn(name="age", type=ColumnType.INTEGER, nullable=True)
            ]
        )

    async def asyncTearDown(self):
        await self.db.disconnect()
        await self._redis.flushdb()
        await self._redis.aclose()


    async def test_connect(self):
        # Already connected in setUp, just check state
        self.assertTrue(self.db._connected)
        self.assertIsNotNone(self.db._db)
        self.assertTrue(await self.db._db.ping())

    async def test_disconnect(self):
        await self.db.disconnect()
        self.assertFalse(self.db._connected)

    async def test_create_table(self):
        await self.db.create_table(self.sample_schema)
        schema_key = f"{self.db.SCHEMA_PREFIX}{self.sample_schema.name}"
        stored_schema = await self._redis.get(schema_key)
        self.assertIsNotNone(stored_schema)
        self.assertEqual(json.loads(stored_schema)["name"], self.sample_schema.name)
        counter_key = f"{self.db.COUNTER_PREFIX}{self.sample_schema.name}:id"
        self.assertEqual(await self._redis.get(counter_key), "0")

    async def test_get_schemas(self):
        await self.db.create_table(self.sample_schema)
        schemas = await self.db.get_schemas()
        self.assertIn("users", schemas)
        self.assertEqual(schemas["users"].name, "users")

    async def test_insert(self):
        await self.db.create_table(self.sample_schema)
        data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        row_id = await self.db.insert("users", data)
        self.assertIsInstance(row_id, str)
        table_key = f"{self.db.TABLE_PREFIX}users"
        stored = await self._redis.hget(table_key, row_id)
        self.assertIsNotNone(stored)
        stored_data = json.loads(stored)
        self.assertEqual(stored_data["name"], "John Doe")
        self.assertEqual(stored_data["age"], "30")

    async def test_get(self):
        await self.db.create_table(self.sample_schema)
        data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        row_id = await self.db.insert("users", data)
        query = SelectQuery(table="users")
        results = await self.db.get(query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "John Doe")
        self.assertEqual(results[0]["age"], 30)

    async def test_update(self):
        await self.db.create_table(self.sample_schema)
        data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        await self.db.insert("users", data)
        update_query = UpdateQuery(
            table="users",
            data={"age": 31},
            where=WhereClause(
                conditions=[
                    Condition(column="email", operator=Operator.EQ, value="john@example.com")
                ]
            )
        )
        updated_count = await self.db.update(update_query)
        self.assertEqual(updated_count, 1)
        query = SelectQuery(table="users")
        results = await self.db.get(query)
        self.assertEqual(results[0]["age"], 31)

    async def test_delete(self):
        await self.db.create_table(self.sample_schema)
        data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        await self.db.insert("users", data)
        delete_query = DeleteQuery(
            table="users",
            where=WhereClause(
                conditions=[
                    Condition(column="email", operator=Operator.EQ, value="john@example.com")
                ]
            )
        )
        deleted_count = await self.db.delete(delete_query)
        self.assertEqual(deleted_count, 1)
        query = SelectQuery(table="users")
        results = await self.db.get(query)
        self.assertEqual(len(results), 0)

    async def test_connection_error_handling(self):
        # Try to connect to a non-existent Redis server
        bad_db = RedisDatabase(host='localhost', port=6390, db=0)
        with self.assertRaises(DBConnectionError):
            await bad_db.connect()

    async def test_not_connected_error(self):
        db = RedisDatabase(host='localhost', port=6379, db=0)
        with self.assertRaises(DBConnectionError):
            await db.get_schemas()


if __name__ == '__main__':
    unittest.main()
