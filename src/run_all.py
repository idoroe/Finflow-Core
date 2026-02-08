"""
run_all.py — The single-command pipeline runner for FinFlow Core.

HIGH-LEVEL EXPLANATION:
    This is the "main" file. When you run `python -m src.run_all`, it executes
    the entire pipeline in the correct order:

      1. Check config & connectivity
      2. Create RAW tables in Snowflake
      3. Load CSV data into RAW tables
      4. Create ANALYTICS tables (star schema)
      5. Transform RAW data into ANALYTICS tables
      6. Run data quality checks
      7. Run demo queries
      8. Capture performance benchmarks

    If any step fails, it stops immediately and logs the error.

WHY THIS MATTERS AT RBC:
    Production pipelines are orchestrated — each step runs in a specific order,
    failures halt the pipeline, and everything is logged. This file is a simple
    version of what tools like Airflow or dbt do at scale.
"""

import sys
import time
import logging

from src.logging_config import setup_logging
from src.config import get_snowflake_config, SQL_DIR
from src.load.snowflake_client import SnowflakeClient
from src.load.load_raw import load_all_csvs
from src.transform.build_analytics import build_analytics_tables
from src.validate.run_quality_checks import run_quality_checks
from src.perf.run_benchmarks import run_benchmarks

logger = setup_logging()


def main():
    """Run the full FinFlow pipeline end-to-end."""
    pipeline_start = time.time()
    logger.info("=" * 60)
    logger.info("FinFlow Core Pipeline — Starting")
    logger.info("=" * 60)

    sf_config = get_snowflake_config()

    with SnowflakeClient(sf_config) as client:
        # Step 1: Set up Snowflake objects (database, schemas, warehouse)
        logger.info("--- Step 1: Snowflake setup ---")
        client.execute_file(SQL_DIR / "00_setup_snowflake.sql")

        # Step 2: Create RAW tables
        logger.info("--- Step 2: Create RAW tables ---")
        client.execute_file(SQL_DIR / "01_create_raw_tables.sql")

        # Step 3: Load CSV data into RAW
        logger.info("--- Step 3: Load data into RAW ---")
        load_all_csvs(client)

        # Step 4 & 5: Build ANALYTICS (create tables + transform)
        logger.info("--- Step 4: Build ANALYTICS layer ---")
        build_analytics_tables(client)

        # Step 6: Quality checks
        logger.info("--- Step 5: Data quality checks ---")
        checks_passed = run_quality_checks(client)
        if not checks_passed:
            logger.error("Quality checks FAILED. Pipeline stopping.")
            sys.exit(1)

        # Step 7 & 8: Demo queries + benchmarks
        logger.info("--- Step 6: Performance benchmarks ---")
        benchmark_results = run_benchmarks(client)

        for result in benchmark_results:
            logger.info("  %s: %.3f sec", result["query"], result["duration_sec"])

    elapsed = time.time() - pipeline_start
    logger.info("=" * 60)
    logger.info("FinFlow Core Pipeline — Complete (%.1f sec)", elapsed)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
