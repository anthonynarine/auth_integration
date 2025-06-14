import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

class ExternalJWTAuthentication(BaseAuthentication):
    """
    Authenticates a user by verifying a JWT token with the external Auth API.
    Attaches user claims to the request as `request.user_claims`.
    """
    
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return None # No token provided, let the other auth classes run
        
        token = auth_header.split(" ")[1]
        
        try:
            response =requests.get(
                f"{settings.AUTH_API_URL}/me/",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5 # Prevent hanging
            )
            
            if response.status_code != 200:
                raise AuthenticationFailed("Invalid or expired token.")
            
            user_claims = response.json()
            request.user_claims = user_claims
