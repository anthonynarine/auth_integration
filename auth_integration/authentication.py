import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from typing import TypedDict, Literal

# ==============================
# 🔐 TypedDict Definitions
# ==============================

class UserClaims(TypedDict):
    """
    Structure of the user object returned by the Auth API `/whoami/` endpoint.
    (Kept compatible with your previous /me/ claims.)
    """
    id: int
    email: str
    role: Literal["admin", "physician", "technologist"]
    first_name: str
    last_name: str

class AuthHeaders(TypedDict):
    Authorization: str


class ExternalJWTAuthentication(BaseAuthentication):
    """
    DRF auth class that validates the incoming request by calling the external
    Auth API "validate" endpoint (default: /whoami/).

    DEV:
      - Bearer <access> is forwarded in the Authorization header.
    PROD:
      - HttpOnly cookies are forwarded via `cookies=request.COOKIES`.

    Configure via Django settings:
      AUTH_API_URL: Base URL (e.g., "https://auth.example.com/api")
      AUTH_API_VALIDATE_PATH: Relative path (default "whoami/")
    """

    timeout = 5  # seconds

    def _validate_url(self) -> str:
        base = (getattr(settings, "AUTH_API_URL", "") or "").rstrip("/")
        path = getattr(settings, "AUTH_API_VALIDATE_PATH", "whoami/").lstrip("/")
        return f"{base}/{path}"

    def authenticate(self, request):
        # 1) Extract bearer, if present (DEV)
        auth_header = request.headers.get("Authorization")
        token = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]

        # 2) Build headers (bearer optional) and forward cookies (for PROD)
        headers: AuthHeaders | dict = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        url = self._validate_url()

        try:
            resp = requests.get(url, headers=headers, cookies=request.COOKIES, timeout=self.timeout)
        except requests.RequestException:
            from auth_integration.exceptions import AuthServiceUnavailable
            raise AuthServiceUnavailable()

        if resp.status_code != 200:
            from auth_integration.exceptions import InvalidTokenError
            raise InvalidTokenError()

        # 3) Attach validated claims to the request and return a placeholder user
        user_claims: UserClaims = resp.json()
        request.user_claims = user_claims
        return (AnonymousUser(), None)
