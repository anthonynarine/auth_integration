"""
auth_integration
----------------
Cross-framework authentication integration for Django + FastAPI.
"""

import importlib
from importlib.util import find_spec

from .client import validate_token, get_claims

__version__ = "0.3.6"

# ---------------------------------------------------------------------
# Permissions Import
# ---------------------------------------------------------------------
require_role = None
if find_spec("auth_integration.permissions"):
    from .permissions import require_role
elif find_spec("auth_integration.django.permissions"):
    from .django.permissions import require_role
else:
    import warnings
    warnings.warn("⚠️ No permissions module found in auth_integration package.")

# ---------------------------------------------------------------------
# Authentication Import (Django / FastAPI autodetect)
# ---------------------------------------------------------------------
ExternalJWTAuth = None

# ✅ Only import Django adapter if Django is installed
if find_spec("django"):
    try:
        from .django.authentication import ExternalJWTAuth
    except Exception as e:
        import warnings
        warnings.warn(f"⚠️ Django detected but import failed: {e}")

# ✅ Otherwise fall back to FastAPI adapter
elif find_spec("auth_integration.fastapi.authentication"):
    from .fastapi.authentication import ExternalJWTAuth
elif find_spec("auth_integration.authentication"):
    from .authentication import ExternalJWTAuth
else:
    import warnings
    warnings.warn("⚠️ No compatible authentication module found in auth_integration package.")

__all__ = [
    "validate_token",
    "ExternalJWTAuth",
    "get_claims",
    "require_role",
]
