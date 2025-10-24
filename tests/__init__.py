# ✅ New Code
# Filename: tests/conftest.py

import pytest
import os

@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Automatically sets GAIT_AUTH_URL for all tests."""
    monkeypatch.setenv("GAIT_AUTH_URL", "https://dummy.example.com/api")
