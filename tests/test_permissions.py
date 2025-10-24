# ✅ New Code
# Filename: tests/test_permissions.py

import pytest
from gait_integration.persmissions import I
from gait_integration.permissions import IsAuthenticated

class MockRequest:
    def __init__(self, user=None):
        self.user = user

@pytest.mark.django_db
def test_authenticated_user_passes_permission():
    """Permission should allow authenticated users."""
    permission = IsAuthenticated()
    request = MockRequest(user="john@example.com")
    assert permission.has_permission(request, None)

@pytest.mark.django_db
def test_anonymous_user_denied_permission():
    """Permission should deny unauthenticated users."""
    permission = IsAuthenticated()
    request = MockRequest(user=None)
    assert not permission.has_permission(request, None)
