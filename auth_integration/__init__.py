"""
auth_integration
----------------
Cross-framework authentication integration for Django + FastAPI.

Exports:
    • validate_token  → direct token validation helper
    • ExternalJWTAuth → main authentication class for API integration
    • get_claims      → dependency for extracting JWT claims
    • require_role    → role-based access dependency
"""

from .client import validate_token, get_claims
from .authentication import ExternalJWTAuth
from .permissions import require_role

__version__ = "0.2.7"

__all__ = [
    "validate_token",
    "ExternalJWTAuth",
    "get_claims",
    "require_role",
]
