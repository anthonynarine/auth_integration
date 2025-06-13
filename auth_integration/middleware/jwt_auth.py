import jwt
import logging
from django.http import JsonResponse
from django.conf import settings
from decouple import config
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

JWT_SECRET = config("JWT_ACCESS_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM", default="HS256")

EXEMPT_PATHS = [
    "/admin/",
    "/api/login/",
    "/api/register/",
    "/api/forgot-password/",
    "/api/reset-password/",
    "/api/token-refresh/",
]

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate users using JWTs from the Auth API.
    Decodes token and injects payload as request.user (dict).
    """

    def process_request(self, request):
        path = request.path_info
        if any(path.startswith(p) for p in EXEMPT_PATHS):
            return None # Let public requests through

        token = None
    
        # 1. Check HttpOnly cookie
        if "access_token" in request.COOKIES:
            token = request.COOKIES["access_token"]

        # 2. Check Authorization header
        elif auth := request.headers.get("Authorization"):
            if auth.startswith("Bearer"):
                token = auth.split(" ")[1]

        if not token:
            logger.warning("JWT: Missing token.")
            return JsonResponse({"detail": "Authentication required."}, status = 401)

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.user = payload # No DB hit - trust the payload
            logger.debug(f"JWT Authenticated user_id={payload.get('user_id')}")
        except jwt.ExpiredSignatureError:
            logger.info("JWT expired.")
            return JsonResponse({"detail": "Token expired."}, status=401)
        except jwt.InvalidTokenError as e:
            logger.warning(f"JWT invalid: {e}")
            return JsonResponse({"detail": "Invalid token."}, status=401)

        return None