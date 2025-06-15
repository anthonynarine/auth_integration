import requests
from rest_framework.authentication import BaseAuthentication
from auth_integration.exceptions import InvalidTokenError, AuthServiceUnavailable
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from typing import TypedDict, Literal


# ==============================
# 🔐 TypedDict Definitions
# ==============================

class UserClaims(TypedDict):
    """
    Structure of the user object returned by the Auth API `/me/` endpoint.
    """
    id: int
    email: str
    role: Literal["admin", "physician", "technologist"]
    first_name: str
    last_name: str

class AuthHeaders(TypedDict):
    """
    HTTP headers required when making the validation request to the Auth API.
    """
    Authorization: str

class ExternalJWTAuthentication(BaseAuthentication):
    """
    Custom DRF authentication class that verifies a JWT access token
    by calling the external Auth API's `/me/` endpoint.

    If valid, attaches user claims to the request as `request.user_claims`.

    Returns:
        - (AnonymousUser, None): If token is valid (we don’t use Django's auth.User)
        - None: If no Authorization header is present (DRF will continue checking)
        - Raises AuthenticationFailed: If token is invalid or Auth API is unreachable
    """

    def authenticate(self, request):
        # Step 1: Get the Authorization header
        auth_header = request.headers.get("Authorization")

        # Step 2: If header is missing or malformed, skip this auth class
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # DRF will try the next auth class (if any)

        # Step 3: Extract the token string
        token = auth_header.split(" ")[1]

        try:
            # Step 4: Define headers and send a request to the external Auth API
            headers: AuthHeaders = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{settings.AUTH_API_URL}/me/",
                headers=headers,
                timeout=5  # Avoid hanging if the Auth API is slow or down
            )

            # Step 5: If the token is invalid or expired, deny access
            if response.status_code != 200:
                raise InvalidTokenError()

            # Step 6: Parse and attach validated user claims to the request
            user_claims: UserClaims = response.json()
            request.user_claims = user_claims

            # Step 7: Return a placeholder user object (we don't use Django's user model)
            return (AnonymousUser(), None)

        except requests.RequestException:
            # Step 8: Fail gracefully if the Auth API is unreachable
            raise AuthServiceUnavailable()