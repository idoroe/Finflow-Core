"""
run_quality_checks.py — Runs data quality checks and fails loudly if any check fails.

HIGH-LEVEL EXPLANATION:
    After loading and transforming data, we need to VERIFY it's correct.
    This file runs a series of SQL queries that look for problems:
      - Are there NULL primary keys? (there shouldn't be)
      - Are there duplicate keys? (there shouldn't be)
      - Do foreign keys in fact tables point to real dimension rows?
      - Are row counts reasonable?

    Each check is a SQL query that returns FAILING rows. If a query returns
    0 rows, the check PASSES. If it returns any rows, something is wrong.

WHY THIS MATTERS AT RBC:
    In banking, bad data = bad decisions = regulatory risk. Data quality checks
    are not optional. Every production pipeline has automated validation.
    If checks fail, the pipeline stops and alerts someone.
"""

import logging
from src.config import SQL_DIR
from src.load.snowflake_client import SnowflakeClient

logger = logging.getLogger("finflow.quality_checks")


def run_quality_checks(client: SnowflakeClient) -> bool:
    """Execute all quality check queries and report results.

    Returns:
        True if ALL checks pass, False if ANY check fails.
    """
    logger.info("=== Running Data Quality Checks ===")

    check_file = SQL_DIR / "04_quality_checks.sql"
    sql_text = check_file.read_text()

    # Each check is separated by a semicolon and should have a comment label
    statements = [s.strip() for s in sql_text.split(";") if s.strip()]

    all_passed = True
    for i, stmt in enumerate(statements, 1):
        # Extract the check name from the first comment line (if present)
        first_line = stmt.split("\n")[0].strip()
        check_name = first_line.lstrip("- ").strip() if first_line.startswith("--") else f"Check {i}"

        cursor = client.conn.cursor()
        try:
            cursor.execute(stmt)
            failures = cursor.fetchall()
            failure_count = len(failures)

            if failure_count == 0:
                logger.info("PASS: %s", check_name)
            else:
                logger.error("FAIL: %s — %d failing row(s) found", check_name, failure_count)
                all_passed = False
        finally:
            cursor.close()

    if all_passed:
        logger.info("=== All quality checks PASSED ===")
    else:
        logger.error("=== Some quality checks FAILED — review errors above ===")

    return all_passed
