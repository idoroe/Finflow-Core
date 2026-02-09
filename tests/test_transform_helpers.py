"""
test_transform_helpers.py — Tests for transformation utility functions.

HIGH-LEVEL EXPLANATION:
    As you add helper functions for data cleaning/transformation in Python,
    add tests here. For now, we test basic data cleaning patterns that
    you'll use throughout the project.
"""

import pandas as pd


def test_uppercase_columns():
    """Column names should be uppercased consistently."""
    df = pd.DataFrame({"name": [1], "Amount": [2], "TOTAL": [3]})
    df.columns = [c.upper() for c in df.columns]
    assert list(df.columns) == ["NAME", "AMOUNT", "TOTAL"]


def test_strip_whitespace_from_strings():
    """String values should have leading/trailing whitespace removed."""
    df = pd.DataFrame({"name": ["  Alice  ", " Bob", "Charlie "]})
    df["name"] = df["name"].str.strip()
    assert list(df["name"]) == ["Alice", "Bob", "Charlie"]


def test_handle_missing_values():
    """NaN values should be detectable."""
    df = pd.DataFrame({"amount": [100, None, 300]})
    assert df["amount"].isna().sum() == 1
