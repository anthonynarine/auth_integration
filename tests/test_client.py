# ✅ New Code
# Filename: tests/test_client.py

import pytest
import httpx
from httpx import Request, Response
from gait_integration.client import validate_token
from gait_integration.exceptions import InvalidTokenError, AuthServiceUnavailable


# ---------------------------------------------------------------------
# 🧩 Async tests require pytest-asyncio
# ---------------------------------------------------------------------
pytestmark = pytest.mark.asyncio


# ---------------------------------------------------------------------
# 🔧 Mock environment
# ---------------------------------------------------------------------
@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """
    Automatically mock GAIT_AUTH_URL and GAIT_TIMEOUT for all tests.
    """
    monkeypatch.setenv("GAIT_AUTH_URL", "https://dummy-auth.com/api")
    monkeypatch.setenv("GAIT_TIMEOUT", "5")


# ---------------------------------------------------------------------
# ✅ Test: Successful token validation (200 OK)
# ---------------------------------------------------------------------
async def test_validate_token_success(httpx_mock):
    """
    Simulate a successful /whoami/ response with valid claims.
    """
    # Step 1: Mock endpoint
    httpx_mock.add_response(
        method="GET",
        url="https://dummy-auth.com/api/whoami/",
        json={
            "id": "user123",
            "email": "tech@example.com",
            "role": "technologist",
            "first_name": "Jane",
            "last_name": "Doe",
        },
        status_code=200,
    )

    # Step 2: Call function
    claims = await validate_token("valid.token")

    # Step 3: Assertions
    assert claims["email"] == "tech@example.com"
    assert claims["role"] == "technologist"


# ---------------------------------------------------------------------
# ❌ Test: Invalid token (401)
# ---------------------------------------------------------------------
async def test_validate_token_invalid(httpx_mock):
    """
    Simulate a 401 Unauthorized response from Auth API.
    """
    httpx_mock.add_response(
        method="GET",
        url="https://dummy-auth.com/api/whoami/",
        status_code=401,
    )

    with pytest.raises(InvalidTokenError):
        await validate_token("invalid.token")


# ---------------------------------------------------------------------
# 🚫 Test: Auth API unreachable (RequestError)
# ---------------------------------------------------------------------
async def test_validate_token_unreachable(monkeypatch):
    """
    Simulate network failure or unreachable Auth API.
    """
    async def mock_get(*args, **kwargs):
        raise httpx.RequestError("Connection failed")

    # Monkeypatch the AsyncClient.get method
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    with pytest.raises(AuthServiceUnavailable):
        await validate_token("any.token")


# ---------------------------------------------------------------------
# ⚠️ Test: Malformed JSON (invalid body on 200)
# ---------------------------------------------------------------------
async def test_validate_token_malformed_json(httpx_mock):
    """
    Simulate a 200 OK but with invalid JSON body.
    """
    httpx_mock.add_response(
        method="GET",
        url="https://dummy-auth.com/api/whoami/",
        text="not-a-json-response",
        status_code=200,
    )

    with pytest.raises(AuthServiceUnavailable):
        await validate_token("valid.token")
