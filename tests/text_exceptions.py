# ✅ New Code
# Filename: tests/test_exceptions.py

import pytest
from gait_integration.exceptions import (
    InvalidTokenError,
    MissingAuthHeaderError,
)

def test_invalid_token_error_message():
    """Ensure InvalidTokenError string output is informative."""
    err = InvalidTokenError("Token expired")
    assert "Token expired" in str(err)

def test_missing_auth_header_error():
    """Ensure MissingAuthHeaderError has proper message."""
    err = MissingAuthHeaderError("Missing header")
    assert "Missing header" in str(err)
