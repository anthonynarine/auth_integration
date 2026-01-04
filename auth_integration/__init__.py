# Filename: auth_integration/__init__.py
"""
auth_integration
----------------
Cross-framework authentication integration for Django + FastAPI.
"""

from __future__ import annotations

from importlib.util import find_spec

from .client import get_claims, validate_token

__version__ = "0.3.7"

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

# ✅ New Code: Prefer Django adapter if Django is installed
if find_spec("django"):
    try:
        # Step 1: Import canonical DRF adapter name
        from .django.authentication import ExternalJWTAuthentication as ExternalJWTAuth
    except Exception:
        # Step 2: Backwards compatibility fallback (older adapter name)
        try:
            from .django.authentication import ExternalJWTAuth  # type: ignore
        except Exception as e:
            import warnings

            warnings.warn(f"⚠️ Django detected but import failed: {e}")

# ✅ Otherwise fall back to FastAPI adapter
elif find_spec("auth_integration.fastapi.authentication"):
    from .fastapi.authentication import ExternalJWTAuth  # type: ignore

# ✅ Otherwise fall back to generic adapter (if present)
elif find_spec("auth_integration.authentication"):
    from .authentication import ExternalJWTAuth  # type: ignore

else:
    import warnings

    warnings.warn("⚠️ No compatible authentication module found in auth_integration package.")


__all__ = [
    "validate_token",
    "ExternalJWTAuth",
    "get_claims",
    "require_role",
]
