"""
config.py — Central configuration loader for FinFlow Core.

HIGH-LEVEL EXPLANATION:
    This file reads your .env file (which has your Snowflake password, account info, etc.)
    and makes those values available to every other Python file in the project.

    Think of it as the "settings page" for the entire pipeline. Instead of hardcoding
    passwords and database names everywhere, every file just imports from here.

WHY THIS MATTERS AT RBC:
    In enterprise environments, credentials and config are NEVER hardcoded. They come
    from environment variables, secret vaults, or config files. This pattern is universal.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root so environment variables are available
# Path(__file__).resolve().parent.parent navigates from src/ up to finflow-core/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_snowflake_config() -> dict:
    """Return a dictionary of Snowflake connection parameters.

    Every key maps to what the Snowflake Python connector expects.
    If any required value is missing, the pipeline will fail fast with a clear error.
    """
    config = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "FINFLOW_XS"),
        "database": os.getenv("SNOWFLAKE_DATABASE", "FINFLOW"),
    }

    # Fail fast: if critical values are missing, stop immediately
    missing = [k for k, v in config.items() if v is None and k in ("account", "user", "password")]
    if missing:
        raise EnvironmentError(
            f"Missing required Snowflake env vars: {missing}. "
            f"Copy .env.example to .env and fill in your credentials."
        )

    return config


# Schema names (used throughout the pipeline)
SCHEMA_RAW = os.getenv("SNOWFLAKE_SCHEMA_RAW", "RAW")
SCHEMA_ANALYTICS = os.getenv("SNOWFLAKE_SCHEMA_ANALYTICS", "ANALYTICS")

# Path to the data/ directory where CSVs live
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))

# Path to the sql/ directory
SQL_DIR = PROJECT_ROOT / "sql"
