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

WHY THIS MATTERS AT RBC:
    Every data pipeline starts by ingesting raw data from somewhere (files, APIs,
    databases). The pattern of "load raw first, transform later" is standard because
    it lets you keep the original data for debugging and auditing.
"""

import logging
import pandas as pd
from pathlib import Path

from src.config import DATA_DIR, SCHEMA_RAW, get_snowflake_config
from src.load.snowflake_client import SnowflakeClient

logger = logging.getLogger("finflow.load_raw")


def load_csv_to_snowflake(client: SnowflakeClient, csv_path: Path, table_name: str):
    """Load a single CSV file into a Snowflake RAW table.

    Strategy: We use Snowflake's write_pandas utility which internally uses
    PUT + COPY INTO — Snowflake's fastest bulk-load method.

    Args:
        client: An active SnowflakeClient connection.
        csv_path: Path to the CSV file.
        table_name: The Snowflake table name to load into (e.g., "TRANSACTIONS").
    """
    logger.info("Reading CSV: %s", csv_path.name)
    df = pd.read_csv(csv_path)
    row_count = len(df)
    logger.info("Read %d rows from %s", row_count, csv_path.name)

    # Normalize column names to uppercase (Snowflake convention)
    df.columns = [col.strip().upper().replace(" ", "_") for col in df.columns]

    # Use write_pandas for efficient bulk loading
    from snowflake.connector.pandas_tools import write_pandas

    logger.info("Loading into %s.%s ...", SCHEMA_RAW, table_name)
    success, num_chunks, num_rows, _ = write_pandas(
        conn=client.conn,
        df=df,
        table_name=table_name,
        schema=SCHEMA_RAW,
        auto_create_table=False,  # We create tables explicitly via SQL scripts
        overwrite=True,           # Truncate + reload for idempotency
    )

    if success:
        logger.info("Loaded %d rows into %s.%s", num_rows, SCHEMA_RAW, table_name)
    else:
        logger.error("Failed to load %s into %s.%s", csv_path.name, SCHEMA_RAW, table_name)
        raise RuntimeError(f"Load failed for {csv_path.name}")


def load_all_csvs(client: SnowflakeClient):
    """Find all CSVs in data/ and load each into its corresponding RAW table.

    Convention: the CSV filename (without extension) becomes the table name.
    Example: data/transactions.csv -> RAW.TRANSACTIONS
    """
    csv_files = sorted(DATA_DIR.glob("*.csv"))

    if not csv_files:
        logger.warning("No CSV files found in %s", DATA_DIR)
        return

    logger.info("Found %d CSV file(s) to load", len(csv_files))

    for csv_path in csv_files:
        table_name = csv_path.stem.upper()  # "transactions.csv" -> "TRANSACTIONS"
        load_csv_to_snowflake(client, csv_path, table_name)

    logger.info("All CSV files loaded into RAW schema.")
