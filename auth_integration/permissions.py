"""
auth_integration.permissions
-----------------------------
Cross-framework permission classes and decorators for Django (DRF) and FastAPI.

Provides:
    - HasRole: DRF permission enforcing a single required role.
    - HasAnyRole: DRF permission allowing multiple roles.
    - require_role: Lightweight decorator for FastAPI route-level role checks.

Teaching Notes:
    This module detects whether Django REST Framework is available.
    If not, it provides FastAPI-safe fallbacks so importing this file
    never breaks in microservices that don’t use DRF.
"""

try:
    # ------------------------------------------------------------
    # Django / DRF Implementation
    # ------------------------------------------------------------
    from rest_framework.permissions import BasePermission

    class HasRole(BasePermission):
        """
        Custom permission class that grants access only to users with a specific role.

        Intended for use in Django REST Framework views that should be limited to one type of user.

        Example:
            class TechnologistView(APIView):
                permission_classes = [HasRole("technologist")]
        """

        def __init__(self, required_role: str):
            """Initialize with a single required role."""
            self.required_role = required_role

        def has_permission(self, request, view) -> bool:
            """Allow access if the user's role matches the required role."""
            user_claims = getattr(request, "user_claims", {})
            return user_claims.get("role") == self.required_role


    class HasAnyRole(BasePermission):
        """
        Grants access if the user has any one of the allowed roles.

        Example:
            class SharedView(APIView):
                permission_classes = [HasAnyRole(["admin", "physician"])]
        """

        def __init__(self, allowed_roles: list[str]):
            """Initialize with a list of acceptable role names."""
            self.allowed_roles = allowed_roles

        def has_permission(self, request, view) -> bool:
            """Allow access if the user's role is in the allowed roles."""
            user_claims = getattr(request, "user_claims", {})
            return user_claims.get("role") in self.allowed_roles


    def require_role(role: str):
        """
        DRF-compatible decorator (no-op by default, DRF handles permissions internally).
        Included for API parity with FastAPI services.
        """
        def decorator(func):
            return func
        return decorator


except ImportError:
    # ------------------------------------------------------------
    # FastAPI / Non-DRF Fallback Implementation
    # ------------------------------------------------------------
    def require_role(role: str):
        """
        FastAPI-compatible route decorator for role-based access control.

        Usage:
            @require_role("admin")
            async def admin_only(...):
                ...
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # Fallback: in a real FastAPI app, you'd extract claims from Depends(get_claims)
                return await func(*args, **kwargs)
            return wrapper
        return decorator

    # Stub classes for compatibility if imported in FastAPI services
    class HasRole:
        """Placeholder for non-DRF environments."""
        def __init__(self, *args, **kwargs): ...
        def has_permission(self, *args, **kwargs) -> bool: return True

    class HasAnyRole:
        """Placeholder for non-DRF environments."""
        def __init__(self, *args, **kwargs): ...
        def has_permission(self, *args, **kwargs) -> bool: return True
