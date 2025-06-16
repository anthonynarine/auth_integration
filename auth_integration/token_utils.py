import os
import requests
from typing import TypedDict, Literal
from .exceptions import InvalidTokenError, AuthServiceUnavailable

class UserClaims(TypedDict):
    id: int
    email: str
    role: Literal["admin", "physician", "technologist"]
    first_name: str
    last_name: str

def verify_token(token: str) -> UserClaims:
    """
    Verifies a JWT access token by calling the external Auth API's `/api/me/` endpoint.

    Expects AUTH_API_URL to be something like: https://your-auth-api.com (no trailing /api)

    Args:
        token (str): JWT access token

    Returns:
        UserClaims: The user claims returned by the Auth API

    Raises:
        InvalidTokenError: If the token is invalid or expired
        AuthServiceUnavailable: If the Auth API cannot be reached
    """
    AUTH_API_URL = os.getenv("AUTH_API_URL")
    if not AUTH_API_URL:
        raise RuntimeError("AUTH_API_URL is not set in environment variables.")

    try:
        url = f"{AUTH_API_URL}/api/me/"
        headers = {"Authorization": f"Bearer {token}"}

        print(f"🔍 [verify_token] Calling {url}")  # Optional debug log
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            raise InvalidTokenError(f"Token rejected with status {response.status_code}")

        return response.json()

    except requests.RequestException as e:
        raise AuthServiceUnavailable(f"Auth service unavailable: {e}")
