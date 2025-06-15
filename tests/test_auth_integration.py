"""
test_auth_integration.py
=========================

Integration test suite for the `auth_integration` package.

Purpose:
--------
These tests verify that the `AuthAPIClient` can communicate correctly
with the deployed Auth API (e.g., https://ant-django-auth.herokuapp.com),
and validate access tokens via the `/whoami/` endpoint.

This test suite does the following:
- Confirms that a valid JWT access token returns user identity and role
- Confirms that an invalid/expired token raises a ValueError
- Skips tests gracefully if tokens are not set in the `.env` file

Usage:
------
1. Create a `.env` file at the project root based on `.env.example`
2. Set the following variables:
    AUTH_API_URL=https://your-auth-api.com
    ACCESS_TOKEN=<valid JWT>
    INVALID_TOKEN=<expired or malformed JWT>

3. Run the tests with:

    $ pytest auth_integration/tests/

Dependencies:
-------------
- python-decouple
- pytest
"""

from auth_integration.client import AuthAPIClient
from decouple import config
import pytest

# Load environment variables
API_URL = config("AUTH_API_URL", default="")
VALID_TOKEN = config("ACCESS_TOKEN", default="")
INVALID_TOKEN = config("INVALID_TOKEN", default="invalid.token.test")


@pytest.mark.skipif(not VALID_TOKEN, reason="No valid token set in .env")
def test_valid_token():
    """
    Validate that a correct JWT access token returns user identity.

    Expects:
    - email and role fields to be present in the response
    """
    client = AuthAPIClient(API_URL)
    user = client.whoami(VALID_TOKEN)
    assert "email" in user
    assert "role" in user


@pytest.mark.skipif(not INVALID_TOKEN, reason="No invalid token set in .env")
def test_invalid_token():
    """
    Validate that an invalid/expired token raises a ValueError with 401.

    Expects:
    - ValueError to be raised
    - Error message to contain "401"
    """
    client = AuthAPIClient(API_URL)
    with pytest.raises(ValueError) as exc:
        client.whoami(INVALID_TOKEN)
    assert "401" in str(exc.value)
