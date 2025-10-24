"""
auth_integration.settings — Unified Configuration Loader
========================================================

Purpose:
--------
This module provides a **universal configuration interface** for the
`auth_integration` package — supporting both Django (via project settings)
and FastAPI (via environment variables using python-decouple).

It ensures that all microservices in the Lumen ecosystem can resolve
authentication settings (e.g., `GAIT_AUTH_URL`, `GAIT_TIMEOUT`) without
framework-specific adapters.

Teaching Notes:
---------------
- Django projects automatically supply settings via `django.conf.settings`.
- FastAPI or standalone services read from `.env` files or environment vars.
- This design keeps configuration consistent across the stack.
"""

import logging
from typing import Optional

# Attempt to import Django settings (if running inside a Django app)
try:
    from django.conf import settings as django_settings
    _is_django = True
except ImportError:
    _is_django = False

# Always import python-decouple for FastAPI and general environment loading
from decouple import config

# -----------------------------------------------------------------------------
# ⚙️ Logger setup (lightweight internal)
# -----------------------------------------------------------------------------
logger = logging.getLogger("auth_integration.settings")
logger.setLevel(logging.INFO)

# -----------------------------------------------------------------------------
# 🔧 Helper: Safe environment or Django setting loader
# -----------------------------------------------------------------------------
def _get_setting(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Attempts to load a configuration variable from:
        1. Django settings (if available)
        2. Environment variables (.env via python-decouple)

    Args:
        name (str): Variable name, e.g., "GAIT_AUTH_URL".
        default (Optional[str]): Fallback value if not found.

    Returns:
        Optional[str]: The loaded value or None if unavailable.
    """
    # Step 1: Django settings (if running under Django)
    if _is_django and hasattr(django_settings, name):
        value = getattr(django_settings, name)
        logger.info(f"Loaded {name} from Django settings.")
        return value

    # Step 2: Environment or .env file
    try:
        value = config(name, default=default)
        if value is not None:
            logger.info(f"Loaded {name} from environment (.env).")
        return value
    except Exception:
        logger.warning(f"{name} not found in settings or environment.")
        return default


# -----------------------------------------------------------------------------
# 🌐 Configuration Variables
# -----------------------------------------------------------------------------
GAIT_AUTH_URL: Optional[str] = _get_setting("GAIT_AUTH_URL") or _get_setting("AUTH_API_URL")
GAIT_TIMEOUT: int = int(_get_setting("GAIT_TIMEOUT", "5"))

# -----------------------------------------------------------------------------
# 🧠 Sanity Check & Safe Logging
# -----------------------------------------------------------------------------
if not GAIT_AUTH_URL:
    logger.warning(
        "⚠️ GAIT_AUTH_URL is not set! Token validation will fail until configured.\n"
        "Set GAIT_AUTH_URL in Django settings or your .env file."
    )
else:
    logger.info(f"✅ GAIT_AUTH_URL loaded successfully (domain only shown): {GAIT_AUTH_URL.split('/')[2]}")
