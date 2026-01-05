# Filename: tests/test_django_authentication.py
import types

import httpx
import pytest
from rest_framework.exceptions import AuthenticationFailed

from auth_integration.django.authentication import (
    ExternalJWTAuthentication,
    ClaimsUser,
    AuthenticationServiceUnavailable,
)


class DummyRequest:
    """Minimal request object for DRF auth testing."""

    def __init__(self, headers=None, meta=None, cookies=None):
        # Step 1: Simulate DRF/Django request interface used by our auth backend
        self.headers = headers or {}
        self.META = meta or {}
        self.COOKIES = cookies or {}


def test_shim_import_path_works():
    """
    Ensure stable import path exists for DRF settings strings.
    """
    # Step 1: Import from public entrypoint
    from auth_integration.authentication import ExternalJWTAuthentication as ShimAuth

    assert ShimAuth is not None


def test_no_credentials_returns_none():
    """
    If no Bearer header and no auth cookies, DRF should treat as anonymous.
    """
    auth = ExternalJWTAuthentication()
    request = DummyRequest(headers={}, cookies={"csrftoken": "x"})  # non-auth cookie

    # Step 1: Should NOT attempt auth based on non-auth cookies
    result = auth.authenticate(request)
    assert result is None


def test_bearer_success_returns_claimsuser_and_claims(monkeypatch):
    """
    Bearer token -> validate_token -> ClaimsUser returned and request.user_claims set.
    """
    auth = ExternalJWTAuthentication()
    request = DummyRequest(headers={"Authorization": "Bearer abc.def.ghi"})

    # Step 1: Mock validate_token used by auth backend (async bridged internally)
    async def mock_validate_token(token: str):
        return {
            "id": "user123",
            "email": "tech@example.com",
            "role": "technologist",
            "first_name": "Jane",
            "last_name": "Doe",
        }

    monkeypatch.setattr(
        "auth_integration.django.authentication.validate_token", mock_validate_token
    )

    user, auth_obj = auth.authenticate(request)

    # Step 2: Validate user object
    assert isinstance(user, ClaimsUser)
    assert user.is_authenticated is True
    assert user.email == "tech@example.com"
    assert user.role == "technologist"

    # Step 3: Validate claims storage
    assert hasattr(request, "user_claims")
    assert request.user_claims["id"] == "user123"

    # Step 4: request.auth should be claims (auth_obj)
    assert auth_obj["email"] == "tech@example.com"


def test_bearer_invalid_raises_authenticationfailed(monkeypatch):
    """
    Invalid Bearer token should map to DRF AuthenticationFailed (401).
    """
    auth = ExternalJWTAuthentication()
    request = DummyRequest(headers={"Authorization": "Bearer bad.token"})

    # Step 1: Mock validate_token to raise InvalidTokenError
    from auth_integration.exceptions import InvalidTokenError

    async def mock_validate_token(token: str):
        raise InvalidTokenError("Invalid or expired token.")

    monkeypatch.setattr(
        "auth_integration.django.authentication.validate_token", mock_validate_token
    )

    with pytest.raises(AuthenticationFailed):
        auth.authenticate(request)


def test_cookie_mode_skips_when_only_non_auth_cookies_present():
    """
    Cookie-mode should NOT run unless access_token/refresh_token/temp_token exists.
    """
    auth = ExternalJWTAuthentication()
    request = DummyRequest(cookies={"csrftoken": "x", "something": "y"})

    # Step 1: With no Bearer and no auth cookies, should return None
    assert auth.authenticate(request) is None


def test_cookie_mode_success(monkeypatch):
    """
    Auth cookies present -> /whoami/ called -> ClaimsUser returned.
    """
    auth = ExternalJWTAuthentication()
    request = DummyRequest(cookies={"access_token": "cookie.jwt.value", "csrftoken": "x"})

    # Step 1: Mock httpx cookie validation response
    class MockResp:
        status_code = 200

        def json(self):
            return {
                "id": "user999",
                "email": "doc@example.com",
                "role": "physician",
                "first_name": "Doc",
                "last_name": "McGee",
            }

    async def mock_get(self, url, cookies):
        return MockResp()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    user, auth_obj = auth.authenticate(request)

    assert isinstance(user, ClaimsUser)
    assert user.role == "physician"
    assert request.user_claims["id"] == "user999"
    assert auth_obj["email"] == "doc@example.com"


def test_cookie_mode_auth_service_unavailable_raises_503(monkeypatch):
    """
    If Gait is unreachable in cookie mode, raise 503 not 401.
    """
    auth = ExternalJWTAuthentication()
    request = DummyRequest(cookies={"access_token": "cookie.jwt.value"})

    async def mock_get(self, url, cookies):
        raise httpx.RequestError("Network down")

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    with pytest.raises(AuthenticationServiceUnavailable):
        auth.authenticate(request)
