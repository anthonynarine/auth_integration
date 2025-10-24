from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    """
    Custom permission class that grants access only to users with a specific role.

    Intended for use in Django REST Framework views that should be limited to one type of user.

    Attributes:
        required_role (str): The single role name required for access (e.g., "admin", "physician", "technologist").

    Example:
        class TechnologistView(APIView):
            permission_classes = [HasRole("technologist")]
    """

    def __init__(self, required_role):
        """
        Initializes the permission class with a required role.

        Args:
            required_role (str): The role that a user must have to access the view.
        """
        self.required_role = required_role

    def has_permission(self, request, view):
        """
        Checks whether the user has the required role to access the view.

        This method is automatically called by Django REST Framework before the view logic runs.

        Args:
            request (HttpRequest): The incoming HTTP request.
            view (APIView): The view being accessed.

        Returns:
            bool: True if user's role matches the required role, False otherwise.
        """
        # Safely access user claims set by your authentication class
        user_claims = getattr(request, "user_claims", {})

        # Compare role in claims to required role
        return user_claims.get("role") == self.required_role


class HasAnyRole(BasePermission):
    """
    Custom permission class that grants access if a user has any one of the allowed roles.

    Useful for views shared between multiple types of users (e.g., admin OR physician).

    Attributes:
        allowed_roles (list): A list of roles allowed to access the view.

    Example:
        class SharedView(APIView):
            permission_classes = [HasAnyRole(["admin", "physician"])]
    """

    def __init__(self, allowed_roles):
        """
        Initializes the permission class with a list of allowed roles.

        Args:
            allowed_roles (list[str]): List of acceptable role names.
        """
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        """
        Checks whether the user's role is in the list of allowed roles.

        Args:
            request (HttpRequest): The incoming HTTP request.
            view (APIView): The view being accessed.

        Returns:
            bool: True if user's role is one of the allowed roles, False otherwise.
        """
        # Safely access user claims set by your authentication class
        user_claims = getattr(request, "user_claims", {})

        # Check if user's role is in the list of allowed roles
        return user_claims.get("role") in self.allowed_roles
