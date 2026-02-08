"""
build_analytics.py — Runs SQL transformations to build the ANALYTICS star schema.

HIGH-LEVEL EXPLANATION:
    This is the "Transform" part of ETL.

    What it does:
      1. Runs the SQL script that creates the ANALYTICS tables (dim_ and fct_ tables)
      2. Runs the SQL script that transforms RAW data into those ANALYTICS tables

    After this step, your data goes from messy staging tables to clean, well-structured
    tables that analysts can query easily.

WHY THIS MATTERS AT RBC:
    The transformation layer is where business logic lives. Raw data is never
    directly queryable by analysts — it needs to be cleaned, joined, and structured.
    This is the core of what data engineers do.

WHAT IS A STAR SCHEMA?
    A star schema organizes data into:
    - FACT tables (fct_): contain measurable events (transactions, orders, etc.)
    - DIMENSION tables (dim_): contain descriptive attributes (customer info, dates, etc.)

    It's called "star" because when you draw the relationships, the fact table sits
    in the center with dimension tables around it like points of a star.
"""

import logging
from src.config import SQL_DIR
from src.load.snowflake_client import SnowflakeClient

logger = logging.getLogger("finflow.build_analytics")


def build_analytics_tables(client: SnowflakeClient):
    """Create analytics tables and populate them from RAW data.

    Runs two SQL scripts in order:
      1. 02_create_analytics_tables.sql — DDL to create dim_ and fct_ tables
      2. 03_transform_raw_to_analytics.sql — INSERT/MERGE statements to populate them
    """
    logger.info("=== Building ANALYTICS layer ===")

    # Step 1: Create the analytics table structures
    create_script = SQL_DIR / "02_create_analytics_tables.sql"
    logger.info("Creating analytics tables...")
    client.execute_file(create_script)

    # Step 2: Transform and load data from RAW into ANALYTICS
    transform_script = SQL_DIR / "03_transform_raw_to_analytics.sql"
    logger.info("Transforming RAW -> ANALYTICS...")
    client.execute_file(transform_script)

    logger.info("=== ANALYTICS layer built successfully ===")
