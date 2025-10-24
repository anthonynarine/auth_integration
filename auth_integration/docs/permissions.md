# 🛡 Auth Integration — permissions.py

## Overview
Provides Django REST Framework (DRF) permission classes based on user roles returned from Gait Auth.

---

## Classes

| Class | Description |
|--------|-------------|
| `HasRole` | Grants access if user role matches the required one |
| `HasAnyRole` | Grants access if user has any role in a list |

---

## Example

```python
from rest_framework.views import APIView
from auth_integration.permissions import HasRole

class PhysicianOnly(APIView):
    permission_classes = [HasRole("physician")]

    def get(self, request):
        return Response({"msg": "Hello Doctor!"})
```

---

Maintained by **Anthony Narine**  
© 2025 — Auth Integration Project
