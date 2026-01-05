# Filename: auth_integration/__init__.py
"""
auth_integration
----------------
Cross-framework authentication integration for Django + FastAPI.

Design rules:
-------------
- Keep package import side-effect free.
- Do NOT import framework-specific modules (Django/DRF/FastAPI) here.
- Downstream services should import adapters from stable entrypoints:
  - DRF:    auth_integration.authentication.ExternalJWTAuthentication
  - FastAPI: auth_integration.fastapi.dependencies.verify_token
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


# ---------------------------------------------------------------------
# 📌 Package Version
# ---------------------------------------------------------------------
# Step 1: Resolve installed version from package metadata (no heavy imports).
try:
    __version__ = version("auth_integration")
except PackageNotFoundError:
    __version__ = "0.0.0"


__all__ = ["__version__"]
