"""
snowflake_client.py — A reusable helper to connect to Snowflake and run SQL.

HIGH-LEVEL EXPLANATION:
    This file creates a "client" — a small wrapper around the Snowflake connector
    that makes it easy to:
      1. Open a connection to Snowflake
      2. Run any SQL statement (CREATE TABLE, INSERT, SELECT, etc.)
      3. Run an entire .sql file
      4. Close the connection cleanly

    Every other module (loader, transformer, validator) uses THIS file to talk
    to Snowflake, so we only write connection logic once.

WHY THIS MATTERS AT RBC:
    You'll see this pattern everywhere — a "database client" class that wraps
    raw connection logic. It keeps your code DRY (Don't Repeat Yourself) and
    makes it easy to swap databases or add retry logic later.
"""

import logging
import snowflake.connector
from pathlib import Path

logger = logging.getLogger("finflow.snowflake_client")


class SnowflakeClient:
    """Manages a single Snowflake connection and provides helper methods."""

    def __init__(self, config: dict):
        """Open a connection to Snowflake using the provided config dict.

        Args:
            config: Dictionary with keys like account, user, password, warehouse, etc.
                    Comes from config.get_snowflake_config().
        """
        self.config = config
        self.conn = None

    def connect(self):
        """Establish the Snowflake connection."""
        logger.info("Connecting to Snowflake account: %s", self.config["account"])
        self.conn = snowflake.connector.connect(**self.config)
        logger.info("Connected successfully.")

    def close(self):
        """Close the Snowflake connection."""
        if self.conn:
            self.conn.close()
            logger.info("Snowflake connection closed.")

    def execute(self, sql: str, params: tuple = None) -> list:
        """Run a single SQL statement and return all result rows.

        Args:
            sql: The SQL string to execute.
            params: Optional tuple of bind parameters (prevents SQL injection).

        Returns:
            A list of tuples — each tuple is one row from the result set.
            For DDL statements (CREATE TABLE, etc.) this will be empty or
            contain a status message.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close()

    def execute_file(self, filepath: Path):
        """Read a .sql file, split it on semicolons, and run each statement.

        This is how we run our SQL scripts (like 01_create_raw_tables.sql).

        Args:
            filepath: Path to the .sql file.
        """
        logger.info("Executing SQL file: %s", filepath.name)
        sql_text = filepath.read_text()

        # Split on semicolons to get individual statements
        statements = [s.strip() for s in sql_text.split(";") if s.strip()]

        for i, stmt in enumerate(statements, 1):
            logger.debug("Running statement %d/%d", i, len(statements))
            self.execute(stmt)

        logger.info("Finished executing %s (%d statements)", filepath.name, len(statements))

    def __enter__(self):
        """Support 'with' statement — automatically connect."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support 'with' statement — automatically close."""
        self.close()
