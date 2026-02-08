"""
test_snowflake_client.py — Tests for the Snowflake client wrapper.

HIGH-LEVEL EXPLANATION:
    We test the SnowflakeClient class WITHOUT actually connecting to Snowflake.
    We use 'mocking' — replacing the real Snowflake connector with a fake one
    that pretends to work. This lets us test our logic without needing a
    real database connection.

    This is a common pattern in enterprise testing.
"""

from unittest.mock import MagicMock, patch
from src.load.snowflake_client import SnowflakeClient


def test_client_connects_and_closes():
    """Client should call connect and close on the Snowflake connector."""
    config = {
        "account": "test",
        "user": "test",
        "password": "test",
        "role": "ACCOUNTADMIN",
        "warehouse": "TEST_WH",
        "database": "TEST_DB",
    }

    with patch("src.load.snowflake_client.snowflake.connector.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        client = SnowflakeClient(config)
        client.connect()

        mock_connect.assert_called_once_with(**config)

        client.close()
        mock_conn.close.assert_called_once()


def test_client_execute_returns_results():
    """Client.execute() should run SQL and return results."""
    config = {"account": "t", "user": "t", "password": "t",
              "role": "t", "warehouse": "t", "database": "t"}

    with patch("src.load.snowflake_client.snowflake.connector.connect") as mock_connect:
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("row1",), ("row2",)]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        client = SnowflakeClient(config)
        client.connect()

        results = client.execute("SELECT 1")

        mock_cursor.execute.assert_called_once_with("SELECT 1", None)
        assert len(results) == 2
