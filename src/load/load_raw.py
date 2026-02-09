"""
load_raw.py — Loads CSV files from the data/ folder into Snowflake RAW tables.

HIGH-LEVEL EXPLANATION:
    This is the "Extract & Load" part of ETL (Extract-Transform-Load).

    What it does:
      1. Finds all CSV files in the data/ directory
      2. For each CSV, reads it into a pandas DataFrame
      3. Uploads (loads) each DataFrame into the matching RAW table in Snowflake

    The RAW tables are "staging" tables — they hold data exactly as it came from
    the CSV, with minimal changes. We clean and transform it later.

    LOADING STRATEGY:
    We use batch INSERT statements. For each CSV we:
      - TRUNCATE the table (wipe old data for idempotency)
      - INSERT rows in batches of 1000 using executemany()
    This is reliable across all network configurations.

WHY THIS MATTERS AT RBC:
    Every data pipeline starts by ingesting raw data from somewhere (files, APIs,
    databases). The pattern of "load raw first, transform later" is standard because
    it lets you keep the original data for debugging and auditing.
"""

import logging
import pandas as pd
from pathlib import Path

from src.config import DATA_DIR, SCHEMA_RAW
from src.load.snowflake_client import SnowflakeClient

logger = logging.getLogger("finflow.load_raw")

BATCH_SIZE = 1000


def load_csv_to_snowflake(client: SnowflakeClient, csv_path: Path, table_name: str):
    """Load a single CSV file into a Snowflake RAW table.

    Strategy: TRUNCATE + batch INSERT using executemany().
    We send rows in chunks of 1000 for efficiency.

    Args:
        client: An active SnowflakeClient connection.
        csv_path: Path to the CSV file.
        table_name: The Snowflake table name to load into (e.g., "ACCOUNT").
    """
    logger.info("Reading CSV: %s", csv_path.name)

    # Try semicolon separator first (Czech banking dataset uses ";"), fall back to comma
    df = pd.read_csv(csv_path, sep=";", low_memory=False)
    if len(df.columns) == 1:
        df = pd.read_csv(csv_path, sep=",", low_memory=False)

    row_count = len(df)
    logger.info("Read %d rows from %s", row_count, csv_path.name)

    # Normalize column names to uppercase (Snowflake convention)
    df.columns = [col.strip().upper().replace(" ", "_") for col in df.columns]

    # Replace NaN with None (Snowflake expects None for NULL, not pandas NaN)
    df = df.where(df.notna(), None)

    # Convert all values to strings (RAW tables are all VARCHAR)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: str(x).strip() if x is not None else None)

    # Quote the table name in case it's a reserved word (like ORDER)
    qualified_table = f'FINFLOW.{SCHEMA_RAW}."{table_name}"'

    # Truncate for idempotency (safe to re-run)
    logger.info("Truncating %s ...", qualified_table)
    client.execute(f'TRUNCATE TABLE {qualified_table}')

    # Build INSERT statement with placeholders
    cols = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_sql = f'INSERT INTO {qualified_table} ({cols}) VALUES ({placeholders})'

    # Insert in batches
    rows = [tuple(row) for row in df.values]
    total_loaded = 0
    cursor = client.conn.cursor()

    try:
        for i in range(0, len(rows), BATCH_SIZE):
            batch = rows[i:i + BATCH_SIZE]
            cursor.executemany(insert_sql, batch)
            total_loaded += len(batch)
            if total_loaded % 10000 == 0 or total_loaded == len(rows):
                logger.info("  %s: %d / %d rows loaded", table_name, total_loaded, len(rows))
    finally:
        cursor.close()

    logger.info("Loaded %d rows into %s", total_loaded, qualified_table)


def load_all_csvs(client: SnowflakeClient):
    """Find all CSVs in data/ and load each into its corresponding RAW table.

    Convention: the CSV filename (without extension) becomes the table name.
    Example: data/account.csv -> RAW.ACCOUNT
    """
    csv_files = sorted(DATA_DIR.glob("*.csv"))

    if not csv_files:
        logger.warning("No CSV files found in %s", DATA_DIR)
        return

    logger.info("Found %d CSV file(s) to load", len(csv_files))

    for csv_path in csv_files:
        table_name = csv_path.stem.upper()
        load_csv_to_snowflake(client, csv_path, table_name)

    logger.info("All CSV files loaded into RAW schema.")
