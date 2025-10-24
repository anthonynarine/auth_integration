# ✅ New Code
# Filename: tests/test_client_integration.py

import pytest
from decouple import config
from gait_integration.client import AuthAPIClient

API_URL = config("AUTH_API_URL", default="")
VALID_TOKEN = config("ACCESS_TOKEN", default="")
INVALID_TOKEN = config("INVALID_TOKEN", default="invalid.token.test")


@pytest.mark.skipif(not VALID_TOKEN, reason="No valid token set in .env")
@pytest.mark.asyncio
async def test_valid_token_live():
    """Validate that a correct JWT access token returns user identity."""
    client = AuthAPIClient(API_URL)
    user = await client.validate_token(VALID_TOKEN)
    assert "email" in user
    assert "role" in user


@pytest.mark.skipif(not INVALID_TOKEN, reason="No invalid token set in .env")
@pytest.mark.asyncio
async def test_invalid_token_live():
    """Validate that an invalid/expired token raises a ValueError."""
    client = AuthAPIClient(API_URL)
    with pytest.raises(ValueError) as exc:
        await client.validate_token(INVALID_TOKEN)
    assert "401" in str(exc.value)
