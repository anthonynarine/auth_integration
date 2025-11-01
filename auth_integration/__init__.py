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

__version__ = "0.3.1"

# ---------------------------------------------------------------------
# Dynamically resolve permission and authentication modules
# ---------------------------------------------------------------------

# ✅ Try importing require_role from the right location
require_role = None
if find_spec("auth_integration.permissions"):
    from .permissions import require_role
elif find_spec("auth_integration.django.permissions"):
    from .django.permissions import require_role
else:
    import warnings
    warnings.warn("⚠️ No permissions module found in auth_integration package.")

# ✅ Dynamically resolve authentication class from available framework
ExternalJWTAuth = None
if find_spec("auth_integration.authentication"):
    from .authentication import ExternalJWTAuth
elif find_spec("auth_integration.django.authentication"):
    from .django.authentication import ExternalJWTAuth
elif find_spec("auth_integration.fastapi.authentication"):
    from .fastapi.authentication import ExternalJWTAuth
else:
    import warnings
    warnings.warn("⚠️ No authentication module found in auth_integration package.")


__all__ = [
    "validate_token",
    "ExternalJWTAuth",
    "get_claims",
    "require_role",
]
