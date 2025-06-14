from typing import Optional
from django.http import HttpRequest

def get_user_claims(request: HttpRequest) -> dict:
    """
    Savely retrieves user clamis attatched to the request by the authentication class. 
    
    Returns an empty dict if clmais are missing.
    """
    return getattr(request, "user_claims", {})


def get_user_id(request: HttpRequest) -> Optional[int]:
    """
    Returns the user's ID from the claims, or None if not present.
    """
    return get_user_claims(request).get("id")

def get_user_role(request: HttpRequest) -> Optional[str]:
    """
    Returns the user's role (e.g., 'admin', 'physician', 'technologist') or None.
    """
    return get_user_claims(request).get("role")


def is_admin(request: HttpRequest) -> bool:
    """
    Returns True if the user is an admin.
    """
    return get_user_role(request) == "admin"


def is_physician(request: HttpRequest) -> bool:
    """
    Returns True if the user is a physician.
    """
    return get_user_role(request) == "physician"

def is_technologist(request: HttpRequest) -> bool:
    """
    Returns True if the user is a technologist.
    """
    return get_user_role(request) == "technologist"
