"""
auth_integration
----------------
Cross-framework authentication integration for Django + FastAPI.

Exports:
    • validate_token  → direct token validation helper
    • ExternalJWTAuth → core class for JWT validation
    • get_claims      → FastAPI dependency
    • require_role    → role-based access dependency
"""

import importlib

# Try to import the shared client + permissions
from .client import validate_token, get_claims
from .permissions import require_role

# Dynamically detect whether Django or FastAPI is in use
try:
    authentication = importlib.import_module("auth_integration.django.authentication")
except ModuleNotFoundError:
    try:
        authentication = importlib.import_module("auth_integration.fastapi.authentication")
    except ModuleNotFoundError:
        authentication = None

if authentication:
    ExternalJWTAuth = getattr(authentication, "ExternalJWTAuth")
else:
    ExternalJWTAuth = None

__version__ = "0.2.9"

__all__ = [
    "validate_token",
    "ExternalJWTAuth",
    "get_claims",
    "require_role",
]
