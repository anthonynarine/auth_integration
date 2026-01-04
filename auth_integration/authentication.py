# Filename: auth_integration/authentication.py
"""
auth_integration.authentication
===============================

Public, stable DRF authentication entrypoint.

Downstream services should reference:
- auth_integration.authentication.ExternalJWTAuthentication

The implementation lives in:
- auth_integration.django.authentication

This re-export layer lets us refactor internal modules without breaking consumers.
"""


from auth_integration.django.authentication import (  
    ClaimsUser,
    ExternalJWTAuthentication,
)
