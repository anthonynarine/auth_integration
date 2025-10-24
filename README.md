# auth_integration

(https://github.com/anthonynarine/Lumen_Authentication/actions/workflows/python-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.2.2-green.svg)](https://github.com/anthonynarine/Lumen_Authentication/releases)


## Overview
`auth_integration` is a reusable authentication integration layer for Django and FastAPI services.
It provides a unified mechanism for validating JWT tokens against an external authentication
provider, such as the Gait Auth API, and for enforcing role‑based permissions.

The package is designed for multi‑service environments where multiple backends (Django, FastAPI, or others)
delegate authentication and identity management to a single authoritative Auth API.

---

## Installation

### Using pip

```bash
pip install git+https://github.com/anthonynarine/auth_integration.git
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
        "auth_integration.authentication.ExternalJWTAuthentication",
    ]
}
```

Add permission classes in your DRF views:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_integration.permissions import HasRole

class TechOnlyView(APIView):
    permission_classes = [HasRole("technologist")]

    def get(self, request):
        return Response({"message": f"Hello, {request.user_claims['email']}"})
```

### FastAPI Example

```python
from fastapi import FastAPI, Depends, HTTPException
from auth_integration.client import validate_token

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
Frontend → Backend (auth_integration) → Gait Auth API (/api/whoami/)
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
