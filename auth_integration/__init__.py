"""
auth_integration
----------------
Cross-framework authentication integration for Django + FastAPI.

Exports:
    • validate_token  → JWT validation helper
    • ExternalJWTAuth → class for verifying tokens via Auth API
    • get_claims      → FastAPI dependency
    • require_role    → role-based access control
"""

import importlib
from importlib.util import find_spec

from .client import validate_token, get_claims
from .permissions import require_role

__version__ = "0.3.0"

# Dynamically resolve authentication class from available framework
ExternalJWTAuth = None

if find_spec("auth_integration.authentication"):
    # Case 1: authentication.py in root (future)
    from .authentication import ExternalJWTAuth
elif find_spec("auth_integration.django.authentication"):
    # Case 2: Django subpackage
    from .django.authentication import ExternalJWTAuth
elif find_spec("auth_integration.fastapi.authentication"):
    # Case 3: FastAPI subpackage
    from .fastapi.authentication import ExternalJWTAuth
else:
    # Graceful fallback
    import warnings
    warnings.warn("⚠️ No authentication module found in auth_integration package.")

__all__ = [
    "validate_token",
    "ExternalJWTAuth",
    "get_claims",
    "require_role",
]
