import unittest
from unittest.mock import Mock, patch, MagicMock
import json

from danielutils.abstractions.db.implementations.redis_database import RedisDatabase
from danielutils.abstractions.db.database_definitions import (
    TableSchema, TableColumn, ColumnType, SelectQuery, UpdateQuery, DeleteQuery,
    WhereClause, Condition, Operator
)


class TestRedisDatabase(unittest.IsolatedAsyncioTestCase):
    """Test cases for RedisDatabase implementation"""

    async def asyncSetUp(self):
        """Set up test fixtures"""
        # Mock redis module
        self.redis_patcher = patch('danielutils.abstractions.db.implementations.redis_database.redis')
        self.mock_redis = self.redis_patcher.start()

        # Create mock Redis client
        self.mock_redis_client = Mock()
        self.mock_redis.Redis.return_value = self.mock_redis_client

        # Create database instance
        self.db = RedisDatabase(host='localhost', port=6379, db=0)

        # Sample schema for testing
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
        """Clean up after tests"""
        self.redis_patcher.stop()

    async def test_connect(self):
        """Test database connection"""
        await self.db.connect()

        self.mock_redis.Redis.assert_called_once_with(
            host='localhost',
            port=6379,
            db=0,
            password=None,
            decode_responses=True
        )
        self.mock_redis_client.ping.assert_called_once()
        self.assertTrue(self.db._connected)

    async def test_disconnect(self):
        """Test database disconnection"""
        self.db._db = self.mock_redis_client
        self.db._connected = True

        await self.db.disconnect()

        self.mock_redis_client.close.assert_called_once()
        self.assertFalse(self.db._connected)

    async def test_create_table(self):
        """Test table creation"""
        self.db._db = self.mock_redis_client
        self.db._connected = True
        self.mock_redis_client.exists.return_value = False

        await self.db.create_table(self.sample_schema)

        # Check that schema was stored
        schema_key = f"{self.db.SCHEMA_PREFIX}{self.sample_schema.name}"
        self.mock_redis_client.set.assert_any_call(
            schema_key, self.sample_schema.to_json())

        # Check that auto-increment counter was initialized
        counter_key = f"{self.db.COUNTER_PREFIX}{self.sample_schema.name}:id"
        self.mock_redis_client.set.assert_any_call(counter_key, 0)

    async def test_get_schemas(self):
        """Test getting all schemas"""
        self.db._db = self.mock_redis_client
        self.db._connected = True

        # Mock schema keys
        schema_keys = [f"{self.db.SCHEMA_PREFIX}users", f"{self.db.SCHEMA_PREFIX}products"]
        self.mock_redis_client.keys.return_value = schema_keys

        # Mock schema data
        schema_json = self.sample_schema.to_json()
        self.mock_redis_client.get.side_effect = [schema_json, None]

        schemas = await self.db.get_schemas()

        self.assertEqual(len(schemas), 1)
        self.assertIn("users", schemas)
        self.assertEqual(schemas["users"].name, "users")

    async def test_insert(self):
        """Test record insertion"""
        self.db._db = self.mock_redis_client
        self.db._connected = True

        # Mock schema retrieval
        schema_json = self.sample_schema.to_json()
        self.mock_redis_client.get.return_value = schema_json

        # Mock auto-increment counter
        self.mock_redis_client.incr.side_effect = [1, 2]  # id counter, row_id counter

        data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        row_id = await self.db.insert("users", data)

        self.assertEqual(row_id, "2")

        # Check that data was stored
        table_key = f"{self.db.TABLE_PREFIX}users"
        expected_data = {
            "id": "1",
            "name": "John Doe",
            "email": "john@example.com",
            "age": "30"
        }
        self.mock_redis_client.hset.assert_called_once_with(table_key, "2", json.dumps(expected_data))

    async def test_get(self):
        """Test record retrieval"""
        self.db._db = self.mock_redis_client
        self.db._connected = True

        # Mock schema retrieval
        schema_json = self.sample_schema.to_json()
        self.mock_redis_client.get.return_value = schema_json

        # Mock table data
        row_data = {
            "id": "1",
            "name": "John Doe",
            "email": "john@example.com",
            "age": "30"
        }
        self.mock_redis_client.hgetall.return_value = {"1": json.dumps(row_data)}

        query = SelectQuery(table="users")
        results = await self.db.get(query)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "John Doe")
        # Should be converted back to int
        self.assertEqual(results[0]["age"], 30)

    async def test_update(self):
        """Test record update"""
        self.db._db = self.mock_redis_client
        self.db._connected = True

        # Mock schema retrieval
        schema_json = self.sample_schema.to_json()
        self.mock_redis_client.get.return_value = schema_json

        # Mock existing table data
        existing_data = {
            "id": "1",
            "name": "John Doe",
            "email": "john@example.com",
            "age": "30"
        }
        self.mock_redis_client.hgetall.return_value = {"1": json.dumps(existing_data)}

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

        # Check that data was updated
        table_key = f"{self.db.TABLE_PREFIX}users"
        expected_data = {
            "id": "1",
            "name": "John Doe",
            "email": "john@example.com",
            "age": "31"
        }
        self.mock_redis_client.hset.assert_called_once_with(table_key, "1", json.dumps(expected_data))

    async def test_delete(self):
        """Test record deletion"""
        self.db._db = self.mock_redis_client
        self.db._connected = True

        # Mock schema retrieval
        schema_json = self.sample_schema.to_json()
        self.mock_redis_client.get.return_value = schema_json

        # Mock existing table data
        existing_data = {
            "id": "1",
            "name": "John Doe",
            "email": "john@example.com",
            "age": "30"
        }
        self.mock_redis_client.hgetall.return_value = {"1": json.dumps(existing_data)}

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

        # Check that data was deleted
        table_key = f"{self.db.TABLE_PREFIX}users"
        self.mock_redis_client.hdel.assert_called_once_with(table_key, "1")

    async def test_connection_error_handling(self):
        """Test connection error handling"""
        self.mock_redis_client.ping.side_effect = self.mock_redis.ConnectionError("Connection failed")

        with self.assertRaises(Exception):
            await self.db.connect()

    async def test_not_connected_error(self):
        """Test error when not connected"""
        with self.assertRaises(Exception):
            await self.db.get_schemas()


if __name__ == '__main__':
    unittest.main()
