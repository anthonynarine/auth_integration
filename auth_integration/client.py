"""
auth_integration.client
=======================

Lightweight client for validating JWT access tokens against the external Auth API.

Purpose
-------
- Intended for *internal services* (e.g. Lumen, Image API) that need to validate
  a user identity but don’t want to re-implement HTTP calls.
- Complements `ExternalJWTAuthentication` (DRF auth class) by providing a
  programmatic API.

⚠️ Important
------------
- This client is *not* responsible for login or token refresh.
- Use it only for identity validation (`/whoami/` or equivalent).

Example
-------
>>> from auth_integration.client import AuthAPIClient
>>> client = AuthAPIClient("https://ant-django-auth-62cf01255868.herokuapp.com/api")
>>> user = client.whoami(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
>>> print(user["email"])
"""

import requests
from typing import TypedDict, Literal
from django.conf import settings


class UserClaims(TypedDict):
    """
    Expected structure of the user data returned by /whoami/ (or configured path).
    """
    id: int
    email: str
    first_name: str
    last_name: str
    role: Literal["admin", "physician", "technologist"]


class AuthAPIClient:
    """
    A simple client for validating access tokens via the Auth API.

    Reads configuration from Django settings if available:
    - AUTH_API_URL ........ Base URL of the Auth API (e.g. https://.../api)
    - AUTH_API_VALIDATE_PATH .. Relative path to validation endpoint (default: whoami/)
    """

    def __init__(self, base_url: str | None = None):
        """
        Initialize the client with the base URL of the Auth API.

        Args:
            base_url (str, optional): Overrides Django settings if provided.
        """
        # Use explicit arg, else fall back to Django settings.
        self.base_url = (base_url or getattr(settings, "AUTH_API_URL", "")).rstrip("/")

    def whoami(self, token: str) -> UserClaims:
        """
        Validate a JWT access token using the configured validation endpoint.

        Args:
            token (str): A raw JWT token (not prefixed with "Bearer").

        Returns:
            UserClaims: Dictionary containing identity claims.

        Raises:
            ValueError: If token is invalid/unauthorized (401).
            RuntimeError: For network errors or unexpected responses.
        """
        # Use configurable path (default "whoami/")
        path = getattr(settings, "AUTH_API_VALIDATE_PATH", "whoami/").lstrip("/")
        url = f"{self.base_url}/{path}"

        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
        except requests.RequestException as e:
            raise RuntimeError(f"Network error contacting Auth API: {e}")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise ValueError("401 Unauthorized: Token is invalid or expired")
        else:
            raise RuntimeError(f"Unexpected response {response.status_code}: {response.text}")
