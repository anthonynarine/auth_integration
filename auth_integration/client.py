"""
auth_integration.client — Unified Async JWT Validation Client
==============================================================

Purpose:
--------
Provides a shared asynchronous client for validating JWT access tokens against
the centralized **Gait Auth API** (`/whoami/` endpoint).

This module replaces the older synchronous `client.py` and `token_utils.py`.
It is fully framework-agnostic and safe for both **Django (DRF)** and **FastAPI**.

Key Features:
-------------
- ✅ Asynchronous, non-blocking (uses httpx)
- ✅ Works across Django & FastAPI
- ✅ Centralized error handling (InvalidTokenError, AuthServiceUnavailable)
- ✅ Secure logging (never logs tokens or PHI)
- ✅ Typed responses via `UserClaims`

Teaching Notes:
---------------
Think of this module as the "trusted messenger" between your backend services
and the Gait Auth API. Its sole job is to verify whether an incoming JWT is
valid — not to issue, refresh, or store tokens.
"""

import logging
import httpx
from typing import TypedDict, Literal

from auth_integration.settings import GAIT_AUTH_URL, GAIT_TIMEOUT
from auth_integration.exceptions import InvalidTokenError, AuthServiceUnavailable


# ============================================================================
# 🧩 TypedDict — expected structure of claims returned by Auth API
# ============================================================================
class UserClaims(TypedDict):
    """
    Expected structure of the claims returned from Gait `/whoami/`.

    Example:
        {
            "id": "user-123",
            "email": "tech@example.com",
            "role": "technologist",
            "first_name": "Jane",
            "last_name": "Doe"
        }
    """
    id: str
    email: str
    role: Literal["admin", "physician", "technologist"]
    first_name: str
    last_name: str


# ============================================================================
# ⚙️ Module-level logger configuration
# ============================================================================
logger = logging.getLogger("auth_integration.client")
logger.setLevel(logging.INFO)


# ============================================================================
# 🔐 Core async validator
# ============================================================================
async def validate_token(token: str) -> UserClaims:
    """
    Validates a JWT access token by calling the Gait Auth API `/whoami/` endpoint.

    Args:
        token (str): The raw JWT access token (without "Bearer" prefix).

    Returns:
        UserClaims: Parsed identity claims from the Auth API.

    Raises:
        InvalidTokenError: If token is invalid, expired, or unauthorized (401).
        AuthServiceUnavailable: If Auth API cannot be reached or returns an unexpected response.

    Teaching Notes:
        - This function performs an asynchronous HTTP GET call.
        - It should be awaited from FastAPI dependencies or called via `asyncio.run()` in Django.
        - Never log or print tokens for HIPAA and security compliance.
    """
    # Step 1: Build the endpoint URL
    url = f"{GAIT_AUTH_URL.rstrip('/')}/whoami/"
    headers = {"Authorization": f"Bearer {token}"}

    logger.info(f"Validating token via {url}")  # Safe: no PHI or token content

    # Step 2: Perform async HTTP GET to Gait
    try:
        async with httpx.AsyncClient(timeout=GAIT_TIMEOUT) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as e:
        logger.error(f"Auth API unreachable: {e.__class__.__name__}")
        raise AuthServiceUnavailable("Authentication service is currently unavailable.") from e

    # Step 3: Handle response cases
    if response.status_code == 200:
        try:
            data = response.json()
            logger.info("✅ Token validated successfully (claims received).")
            return data  # type: ignore
        except Exception:
            logger.error("Invalid JSON response from Auth API.")
            raise AuthServiceUnavailable("Malformed response from authentication service.")
    elif response.status_code == 401:
        logger.warning("Invalid or expired token received (401).")
        raise InvalidTokenError("Invalid or expired token.")
    else:
        logger.error(f"Unexpected status {response.status_code} from Auth API.")
        raise AuthServiceUnavailable(f"Unexpected response: {response.status_code}")
