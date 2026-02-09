"""
test_config.py — Tests for the configuration loader.

HIGH-LEVEL EXPLANATION:
    These tests verify that config.py correctly reads environment variables
    and fails with a clear error when required values are missing.

    We use 'monkeypatch' (a pytest feature) to temporarily set or unset
    environment variables during tests without affecting the real environment.
"""

import pytest
from unittest.mock import patch


def test_get_snowflake_config_with_valid_env():
    """Config should return a dict when all required env vars are set."""
    env = {
        "SNOWFLAKE_ACCOUNT": "test_account",
        "SNOWFLAKE_USER": "test_user",
        "SNOWFLAKE_PASSWORD": "test_pass",
    }
    with patch.dict("os.environ", env, clear=False):
        from src.config import get_snowflake_config
        config = get_snowflake_config()

        assert config["account"] == "test_account"
        assert config["user"] == "test_user"
        assert config["password"] == "test_pass"


def test_get_snowflake_config_missing_account():
    """Config should raise an error when SNOWFLAKE_ACCOUNT is missing."""
    with patch("src.config.os.getenv", side_effect=lambda key, default=None: {
        "SNOWFLAKE_USER": None,
        "SNOWFLAKE_PASSWORD": None,
        "SNOWFLAKE_ACCOUNT": None,
    }.get(key, default)):
        from src.config import get_snowflake_config
        with pytest.raises(EnvironmentError, match="Missing required"):
            get_snowflake_config()
