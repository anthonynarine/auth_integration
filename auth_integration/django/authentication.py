"""
auth_integration.django.authentication — DRF Adapter
====================================================

Purpose:
--------
Django REST Framework (DRF) authentication backend that validates an incoming
request against the centralized Gait Auth API. It supports:

1) DEV/Bearer Mode:
   - Reads "Authorization: Bearer <token>" from headers.
   - Uses the shared async validator `validate_token()` (httpx) to call `/whoami/`.

2) PROD/Cookie Mode (HttpOnly cookies):
   - If no Bearer header is present, forwards request.COOKIES directly to Gait
     for `/whoami/` validation via an async httpx call from this adapter.

On success, attaches `request.user_claims` and returns `(AnonymousUser(), None)`.

Security:
---------
- Never logs tokens or PHI.
- Logs only high-level validation events and HTTP codes.

Teaching Notes:
---------------
- This class is sync (DRF), but it safely bridges into async using
  `asgiref.sync.async_to_sync(...)` so we can re-use the async validator.
"""

from __future__ import annotations

import logging
from typing import TypedDict, Literal, Optional

import httpx
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from asgiref.sync import async_to_sync

from auth_integration.settings import GAIT_AUTH_URL, GAIT_TIMEOUT
from auth_integration.exceptions import InvalidTokenError, AuthServiceUnavailable
from auth_integration.client import validate_token  # async validator


# -----------------------------------------------------------------------------
# 🧩 Types
# -----------------------------------------------------------------------------
class UserClaims(TypedDict):
    id: str
    email: str
    role: Literal["admin", "physician", "technologist"]
    first_name: str
    last_name: str


# -----------------------------------------------------------------------------
# ⚙️ Logger (HIPAA-safe)
# -----------------------------------------------------------------------------
logger = logging.getLogger("auth_integration.django.authentication")
logger.setLevel(logging.INFO)


# -----------------------------------------------------------------------------
# 🔧 Helpers
# -----------------------------------------------------------------------------
def _extract_bearer_token(request) -> Optional[str]:
    """
    Extract a raw JWT from the Authorization header (if present).

    Returns:
        Optional[str]: The token string without the "Bearer " prefix, or None.
    """
    auth_header = request.headers.get("Authorization") or request.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        return None

    # Accept "Bearer <token>" (case-insensitive prefix)
    parts = auth_header.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1].strip()

    return None


async def _validate_with_cookies(cookies: dict) -> UserClaims:
    """
    Validate the session by forwarding HttpOnly cookies to the Gait /whoami/.

    This is used in PROD when the frontend does not expose the token and relies on cookies.

    Args:
        cookies (dict): Django request.COOKIES (forwarded as-is).

    Returns:
        UserClaims: Validated claims.

    Raises:
        InvalidTokenError: If Gait returns 401.
        AuthServiceUnavailable: If Gait is unreachable or misconfigured.
    """
    if not GAIT_AUTH_URL:
        logger.error("Missing GAIT_AUTH_URL — cannot validate cookies.")
        raise AuthServiceUnavailable("Authentication service misconfigured.")

    url = f"{GAIT_AUTH_URL.rstrip('/')}/whoami/"
    logger.info("Validating session via cookies at /whoami/ (no PHI logged).")

    try:
        async with httpx.AsyncClient(timeout=GAIT_TIMEOUT) as client:
            resp = await client.get(url, cookies=cookies)
    except httpx.RequestError:
        logger.error("Auth API unreachable while validating cookies.")
        raise AuthServiceUnavailable()

    if resp.status_code == 200:
        try:
            return resp.json()  # type: ignore[return-value]
        except Exception:
            logger.error("Malformed JSON from Auth API during cookie validation.")
            raise AuthServiceUnavailable("Malformed response from authentication service.")

    if resp.status_code == 401:
        logger.warning("Cookie-based validation failed with 401.")
        raise InvalidTokenError("Invalid or expired session.")

    logger.error("Unexpected status from Auth API during cookie validation: %s", resp.status_code)
    raise AuthServiceUnavailable(f"Unexpected response: {resp.status_code}")


# -----------------------------------------------------------------------------
# 🔐 DRF Authentication Class
# -----------------------------------------------------------------------------
class ExternalJWTAuthentication(BaseAuthentication):
    """
    DRF authentication backend delegating JWT/session validation to Gait Auth API.

    DEV (Bearer):
        - Reads Authorization header (Bearer).
        - Uses shared async validator: validate_token(token).

    PROD (HttpOnly cookies):
        - If no Bearer present, forwards request.COOKIES to Gait /whoami/ via async httpx.

    On success:
        - Attaches `request.user_claims`.
        - Returns (AnonymousUser(), None) to indicate external identity verification.

    Raises:
        InvalidTokenError (401) or AuthServiceUnavailable (503) mapped via DRF.
    """

    def authenticate(self, request):
        # Step 1: Try Authorization Bearer (DEV)
        token = _extract_bearer_token(request)

        try:
            if token:
                logger.info("Bearer token detected — validating via shared async client.")
                # Bridge async validator into sync context safely
                claims: UserClaims = async_to_sync(validate_token)(token)
            else:
                # Step 2: Cookie mode (PROD with HttpOnly cookies)
                logger.info("No Bearer token — attempting cookie-based validation.")
                claims = async_to_sync(_validate_with_cookies)(request.COOKIES)

        except InvalidTokenError as e:
            # DRF expects AuthenticationFailed for 401
            raise AuthenticationFailed(str(e))  # 401
        except AuthServiceUnavailable as e:
            # Map to DRF exception; HTTP 503 upstream via exception handler
            raise AuthenticationFailed(str(e))  # Keep as 401 for DRF default handling
        except Exception as e:
            logger.error("Unexpected error during authentication: %s", e.__class__.__name__)
            raise AuthenticationFailed("Authentication error.")

        # Step 3: Attach claims & return placeholder user
        request.user_claims = claims
        return (AnonymousUser(), None)
