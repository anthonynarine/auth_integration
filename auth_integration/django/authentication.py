# Filename: auth_integration/django/authentication.py
"""
auth_integration.django.authentication — DRF Adapter
====================================================

Purpose:
--------
Django REST Framework (DRF) authentication backend that validates requests
against the centralized Gait Auth API (/whoami/).

Modes:
------
1) DEV/Bearer Mode:
   - Reads "Authorization: Bearer <token>".
   - Validates via shared async validator `validate_token(token)`.

2) PROD/Cookie Mode:
   - If no Bearer token is present, forwards request.COOKIES to Gait /whoami/.

On success:
-----------
- Attaches `request.user_claims` (dict)
- Returns a lightweight authenticated `ClaimsUser` object for DRF permission checks.

Security & Privacy:
-------------------
- Never logs tokens or cookies.
- Treats malformed claim payloads as auth failures (fail closed).
- Keeps cache keys hashed (sha256(token)) — never stores raw tokens.

Performance:
------------
- Optional short TTL cache for Bearer validations to reduce /whoami/ calls.

Teaching Notes:
---------------
- DRF authentication backends are sync; we bridge async calls using `async_to_sync`.
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass
from typing import Literal, Optional, TypedDict, cast

import httpx
from asgiref.sync import async_to_sync
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException, AuthenticationFailed

from auth_integration.client import validate_token  # async validator
from auth_integration.exceptions import AuthServiceUnavailable, InvalidTokenError
from auth_integration.settings import GAIT_AUTH_URL, GAIT_TIMEOUT

# -----------------------------------------------------------------------------
# ⚙️ Logger (HIPAA-safe)
# -----------------------------------------------------------------------------
logger = logging.getLogger("auth_integration.django.authentication")


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
# ✅ Claims-backed "User" for DRF
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class ClaimsUser:
    """Lightweight authenticated user backed by validated claims."""

    id: str
    email: str
    role: Literal["admin", "physician", "technologist"]
    first_name: str
    last_name: str

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self) -> str:
        label = self.email or self.id
        return f"{label} ({self.role})"


# -----------------------------------------------------------------------------
# 🧯 DRF Exception for upstream auth outage
# -----------------------------------------------------------------------------
class AuthenticationServiceUnavailable(APIException):
    """Raised when the upstream Auth API is unreachable or misconfigured."""

    status_code = 503
    default_detail = "Authentication service unavailable."
    default_code = "auth_service_unavailable"


# -----------------------------------------------------------------------------
# 🚀 Tiny in-process TTL cache for Bearer validations (speed win)
# -----------------------------------------------------------------------------
# Key: sha256(token), Value: (expires_at_epoch, claims_dict)
_BEARER_CACHE: dict[str, tuple[float, UserClaims]] = {}
_BEARER_CACHE_MAX = 2048
_BEARER_CACHE_TTL_SECONDS = 45


def _hash_token(token: str) -> str:
    """Hash token for cache keying without storing the raw token."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _cache_get(token: str) -> Optional[UserClaims]:
    """# Step 1: Return cached claims if present and not expired."""
    now = time.time()
    key = _hash_token(token)
    item = _BEARER_CACHE.get(key)
    if not item:
        return None

    expires_at, claims = item
    if expires_at <= now:
        _BEARER_CACHE.pop(key, None)
        return None

    return claims


def _cache_set(token: str, claims: UserClaims) -> None:
    """# Step 2: Store claims in cache with TTL; evict oldest opportunistically."""
    if _BEARER_CACHE_MAX <= 0 or _BEARER_CACHE_TTL_SECONDS <= 0:
        return

    if len(_BEARER_CACHE) >= _BEARER_CACHE_MAX:
        # Evict one arbitrary item (simple + fast). For LRU, add dependency later.
        _BEARER_CACHE.pop(next(iter(_BEARER_CACHE)), None)

    key = _hash_token(token)
    _BEARER_CACHE[key] = (time.time() + _BEARER_CACHE_TTL_SECONDS, claims)


# -----------------------------------------------------------------------------
# 🔧 Helpers
# -----------------------------------------------------------------------------
def _extract_bearer_token(request) -> Optional[str]:
    """Extract token from Authorization header if present."""
    auth_header = request.headers.get("Authorization") or request.META.get(
        "HTTP_AUTHORIZATION"
    )
    if not auth_header:
        return None

    parts = auth_header.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1].strip()
        return token or None

    return None


def _validate_claims_shape(raw: object) -> UserClaims:
    """# Step 3: Validate the claim payload shape (fail closed).

    Args:
        raw: The parsed JSON object returned by Gait.

    Returns:
        UserClaims: A validated claims dict.

    Raises:
        AuthenticationFailed: If payload is missing required keys.
    """
    if not isinstance(raw, dict):
        raise AuthenticationFailed("Invalid authentication response.")

    required = ("id", "email", "role", "first_name", "last_name")
    for key in required:
        if key not in raw:
            raise AuthenticationFailed("Invalid authentication response.")

    role = raw.get("role")
    if role not in ("admin", "physician", "technologist"):
        raise AuthenticationFailed("Invalid authentication response.")

    return cast(UserClaims, raw)


async def _validate_with_cookies(cookies: dict) -> UserClaims:
    """Validate session by forwarding HttpOnly cookies to Gait /whoami/."""
    if not GAIT_AUTH_URL:
        raise AuthServiceUnavailable("Missing GAIT_AUTH_URL.")

    url = f"{GAIT_AUTH_URL.rstrip('/')}/whoami/"

    try:
        async with httpx.AsyncClient(timeout=GAIT_TIMEOUT) as client:
            resp = await client.get(url, cookies=cookies)
    except httpx.RequestError:
        raise AuthServiceUnavailable("Auth API unreachable.")

    if resp.status_code == 200:
        try:
            return _validate_claims_shape(resp.json())
        except ValueError:
            raise AuthServiceUnavailable("Malformed JSON from auth service.")

    if resp.status_code == 401:
        raise InvalidTokenError("Invalid or expired session.")

    raise AuthServiceUnavailable(f"Unexpected auth response: {resp.status_code}")


# -----------------------------------------------------------------------------
# 🔐 DRF Authentication Class
# -----------------------------------------------------------------------------
class ExternalJWTAuthentication(BaseAuthentication):
    """DRF auth backend delegating validation to Gait Auth API."""

    def authenticate_header(self, request) -> str:
        return "Bearer"

    def authenticate(self, request):
        # Step 1: Determine credentials source
        token = _extract_bearer_token(request)
        cookies = getattr(request, "COOKIES", None) or {}

        # Step 2: No credentials => DRF should treat as unauthenticated (not error)
        if not token and not cookies:
            return None

        # Step 3: Validate
        try:
            if token:
                # Step 3.1: Cache fast-path
                cached = _cache_get(token)
                if cached:
                    claims = cached
                else:
                    raw_claims = async_to_sync(validate_token)(token)
                    claims = _validate_claims_shape(raw_claims)
                    _cache_set(token, claims)
            else:
                claims = async_to_sync(_validate_with_cookies)(cookies)

        except InvalidTokenError as e:
            raise AuthenticationFailed(str(e))  # 401
        except AuthServiceUnavailable as e:
            raise AuthenticationServiceUnavailable(str(e))  # 503
        except AuthenticationFailed:
            # Pass-through (already a 401)
            raise
        except Exception as e:
            logger.error("Unexpected auth error: %s", e.__class__.__name__)
            raise AuthenticationFailed("Authentication error.")  # 401

        # Step 4: Attach claims for RBAC & return authenticated user
        request.user_claims = claims
        user = ClaimsUser(
            id=claims["id"],
            email=claims["email"],
            role=claims["role"],
            first_name=claims["first_name"],
            last_name=claims["last_name"],
        )

        return (user, token)
