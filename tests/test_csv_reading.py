"""
test_csv_reading.py — Tests that CSV files can be read correctly.

HIGH-LEVEL EXPLANATION:
    Before loading data to Snowflake, we should verify that:
    - CSV files exist in the data/ directory
    - They can be read without errors
    - They have the expected columns

    These tests use a small temporary CSV file (created during the test)
    so they don't depend on real data being present.
"""

import pandas as pd
import tempfile
from pathlib import Path


def test_read_csv_basic():
    """A basic CSV should be readable with pandas."""
    csv_content = "id,name,amount\n1,Alice,100.50\n2,Bob,200.75\n"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        f.flush()
        df = pd.read_csv(f.name)

    assert len(df) == 2
    assert list(df.columns) == ["id", "name", "amount"]


def test_column_normalization():
    """Column names should be normalizable to uppercase with underscores."""
    csv_content = "First Name,last name,Total Amount\n1,2,3\n"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        f.flush()
        df = pd.read_csv(f.name)

    df.columns = [col.strip().upper().replace(" ", "_") for col in df.columns]
    assert list(df.columns) == ["FIRST_NAME", "LAST_NAME", "TOTAL_AMOUNT"]
