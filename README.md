# gait_integration

## Overview
`gait_integration` is a reusable authentication integration layer for Django and FastAPI services.
It provides a unified mechanism for validating JWT tokens against an external authentication
provider, such as the Gait Auth API, and for enforcing role‑based permissions.

The package is designed for multi‑service environments where multiple backends (Django, FastAPI, or others)
delegate authentication and identity management to a single authoritative Auth API.

---

## Installation

### Using pip

```bash
pip install git+https://github.com/anthonynarine/gait_integration.git
```

### Requirements

- Python 3.10+
- Django 4.0+ or FastAPI 0.100+
- `requests`, `python-decouple`, and `PyJWT`

---

## Configuration

### Django Example

In `settings.py`:

```python
AUTH_API_URL = "https://gait.example.com/api"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "gait_integration.authentication.ExternalJWTAuthentication",
    ]
}
```

Add permission classes in your DRF views:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from gait_integration.permissions import HasRole

class TechOnlyView(APIView):
    permission_classes = [HasRole("technologist")]

    def get(self, request):
        return Response({"message": f"Hello, {request.user_claims['email']}"})
```

### FastAPI Example

```python
from fastapi import FastAPI, Depends, HTTPException
from gait_integration.client import validate_token

app = FastAPI()

@app.get("/secure-endpoint")
async def secure_endpoint(token: str):
    claims = await validate_token(token)
    return {"user": claims}
```

---

## Architecture

Each service delegates token validation to the central Gait Auth API:

```
Frontend → Backend (gait_integration) → Gait Auth API (/api/whoami/)
```

The backend receives user claims from Gait and attaches them to the request context
for authorization checks.

---

## Testing

Refer to `TESTING_GUIDE.md` for details on the unit and integration test coverage.
---

## Maintainer

Maintained by **Anthony Narine**  
© 2025 — Released under the MIT License
