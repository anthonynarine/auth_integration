"""
auth_integration.client
=======================

Provides an AuthAPIClient for validating JWT access tokens using an external Auth API.
This client is designed to be used by internal services like Lumen, Image API, etc.

This client should NOT be used to handle login or token refresh — only identity validation.

Example usage:
--------------
>>> client = AuthAPIClient("https://your-auth-api.com")
>>> user = client.whoami(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
>>> print(user["email"])
"""

import requests
from typing import TypedDict, Literal


class UserClaims(TypedDict):
    """
    Expected structure of the user data returned by /whoami/
    """
    id: int
    email: str
    first_name: str
    last_name: str
    role: Literal["admin", "physician", "technologist"]


class AuthAPIClient:
    """
    A simple client for validating access tokens via the /whoami/ endpoint of the Auth API.
    """

    def __init__(self, base_url: str):
        """
        Initialize the client with the base URL of the Auth API.
        Args:
            base_url (str): e.g. "https://ant-django-auth.herokuapp.com"
        """
        self.base_url = base_url.rstrip("/")

    def whoami(self, token: str) -> UserClaims:
        """
        Validates a JWT access token using /whoami/ endpoint.

        Args:
            token (str): A raw JWT token (not prefixed with "Bearer")

        Returns:
            UserClaims: dictionary containing user identity and role

        Raises:
            ValueError: If token is invalid or unauthorized (401)
            RuntimeError: For network errors or unexpected responses
        """
        url = f"{self.base_url}/whoami/"
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
