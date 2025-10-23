from rest_framework.exceptions import APIException


class AuthServiceUnavailable(APIException):
    """
    Raised when the external Auth API is unreachable or times out.
    """
    status_code = 503
    default_detail = "Authentication service is currently unavailable."
    default_code = "auth_service_unavailable"


class InvalidTokenError(APIException):
    """
    Raised when the provided JWT is invalid, expired, or unauthorized.
    """
    status_code = 401
    default_detail = "Invalid or expired token."
    default_code = "invalid_token"
