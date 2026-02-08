"""
run_benchmarks.py — Times key queries to measure pipeline performance.

HIGH-LEVEL EXPLANATION:
    This file measures how long things take:
      - How long do the demo analytics queries run?
      - What's the total pipeline time?

    You'll run this BEFORE optimizing, record the numbers, then optimize
    (add a clustering key, rewrite a query, etc.) and run again to show
    the improvement.

WHY THIS MATTERS AT RBC:
    Enterprise data teams care deeply about query performance. Slow queries
    cost money (Snowflake charges by compute time) and frustrate users.
    Being able to measure, optimize, and PROVE improvement is a key skill.
"""

import logging
import time
from src.config import SQL_DIR
from src.load.snowflake_client import SnowflakeClient

logger = logging.getLogger("finflow.benchmarks")


def run_benchmarks(client: SnowflakeClient) -> list[dict]:
    """Time each demo query and return results.

    Returns:
        A list of dicts like: [{"query": "...", "duration_sec": 1.23}, ...]
    """
    logger.info("=== Running Performance Benchmarks ===")

    demo_file = SQL_DIR / "05_demo_queries.sql"
    sql_text = demo_file.read_text()

    statements = [s.strip() for s in sql_text.split(";") if s.strip()]
    results = []

    for i, stmt in enumerate(statements, 1):
        first_line = stmt.split("\n")[0].strip()
        query_name = first_line.lstrip("- ").strip() if first_line.startswith("--") else f"Query {i}"

        start = time.time()
        client.execute(stmt)
        elapsed = time.time() - start

        results.append({"query": query_name, "duration_sec": round(elapsed, 3)})
        logger.info("%-50s  %.3f sec", query_name, elapsed)

    logger.info("=== Benchmarks complete ===")
    return results
