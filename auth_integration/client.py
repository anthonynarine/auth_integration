"""
auth_integration.client — Unified Async JWT Validation Client
==============================================================

Purpose:
--------
Provides a shared asynchronous client for validating JWT access tokens against
the centralized **Gait Auth API** (`/whoami/` endpoint).

Fully framework-agnostic — works with both **Django (DRF)** and **FastAPI**.

Key Features:
-------------
- ✅ Asynchronous (uses httpx)
- ✅ Works across Django & FastAPI
- ✅ Optional dependency helper for FastAPI (get_claims)
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
from typing import TypedDict, Literal, Dict, Any, Optional
from fastapi import Depends, Header, HTTPException, status

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
        - Performs asynchronous HTTP GET call using httpx.
        - Never log or print tokens for HIPAA and security compliance.
    """
    url = f"{GAIT_AUTH_URL.rstrip('/')}/whoami/"
    headers = {"Authorization": f"Bearer {token}"}

    logger.info(f"Validating token via {url}")  # Safe: no PHI or token content

    try:
        async with httpx.AsyncClient(timeout=GAIT_TIMEOUT) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as e:
        logger.error(f"Auth API unreachable: {e.__class__.__name__}")
        raise AuthServiceUnavailable("Authentication service is currently unavailable.") from e

    if response.status_code == 200:
        try:
            data = response.json()
            logger.info("✅ Token validated successfully (claims received).")
            return data  # type: ignore
        except Exception as e:
            logger.error(f"Invalid JSON response: {e}")
            raise AuthServiceUnavailable("Malformed response from authentication service.")
    elif response.status_code == 401:
        logger.warning("Invalid or expired token received (401).")
        raise InvalidTokenError("Invalid or expired token.")
    else:
        logger.error(f"Unexpected status {response.status_code} from Auth API.")
        raise AuthServiceUnavailable(f"Unexpected response: {response.status_code}")


# ============================================================================
# ⚡ FastAPI Dependency: Extract & validate token from Authorization header
# ============================================================================
async def get_claims(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    FastAPI dependency that extracts a Bearer token from the Authorization header
    and returns the validated user claims.

    Example:
        @app.get("/whoami")
        async def whoami(claims: dict = Depends(get_claims)):
            return claims
    """
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Missing or invalid Authorization header.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid.",
        )

    token = authorization.split("Bearer ")[1].strip()
    try:
        return await validate_token(token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except AuthServiceUnavailable as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
