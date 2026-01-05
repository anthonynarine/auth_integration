# auth_integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.3.8-green.svg)](https://github.com/anthonynarine/Lumen_Authentication/releases)

Reusable authentication adapter for **Django REST Framework** and **FastAPI** services that delegate
authentication to a single external Auth API (e.g., **Gait**).

---

## Why this exists

In multi-service systems, you often want **one source of truth** for identity and roles:

- Auth service owns users, passwords, 2FA, token issuance, and sessions.
- Downstream services (reports, media, AI, HL7, etc.) should **only validate** the incoming request
  and then use the returned **claims** for authorization.

`auth_integration` is the lightweight “adapter” layer that makes that easy across frameworks.

---

## What you get

### Django REST Framework (DRF)
- A DRF authentication backend: `ExternalJWTAuthentication`
- Returns an authenticated `ClaimsUser` (no local DB user required)
- Attaches `request.user_claims` for downstream permissions and auditing
- Supports:
  - **Bearer mode** (Authorization header)
  - **Cookie mode** (HttpOnly cookies forwarded to `/whoami/`)

### FastAPI
- A dependency helper (see `auth_integration.fastapi.dependencies`)
- Validates Bearer tokens against `/whoami/` and returns claims for your routes

---

## Claims contract

`/api/whoami/` is expected to return at least:

- `id`
- `first_name`
- `last_name`
- `email`
- `role` (`admin` | `physician` | `technologist`)
- `is_2fa_enabled`

> Passwords are never returned.

---

## Installation

### pip (git tag install)

```bash
pip install "auth_integration @ git+https://github.com/anthonynarine/auth_integration.git@v0.3.8"
```

### Requirements
- Python 3.10+
- Django + DRF **or** FastAPI
- `httpx`
- `asgiref` (Django/DRF adapter)
- `python-decouple` (recommended for env config)

---

## Configuration

### Environment variables (recommended)
Set these in your service environment:

- `GAIT_AUTH_URL` — Base URL of the Auth API (example: `https://.../api`)
- `GAIT_TIMEOUT` — HTTP timeout (seconds)

> These are read by `auth_integration.settings`.

---

## Django (DRF) quickstart

### 1) Configure DRF authentication

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Stable public entrypoint (recommended)
        "auth_integration.authentication.ExternalJWTAuthentication",
    ],
}
```

### 2) Use `request.user` + `request.user_claims`

```python
# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "user": str(request.user),
                "claims": getattr(request, "user_claims", None),
            }
        )
```

### Cookie mode (HttpOnly sessions)
If no `Authorization: Bearer ...` header is present, the DRF adapter can validate by forwarding
auth cookies to `/whoami/`.

To keep this fast and predictable, cookie-mode validation only runs when at least one of these
cookies exists:

- `access_token`
- `refresh_token`
- `temp_token`

---

## FastAPI quickstart

```python
from fastapi import FastAPI, Depends
from auth_integration.fastapi.dependencies import verify_token

app = FastAPI()

@app.get("/secure")
async def secure_endpoint(claims=Depends(verify_token)):
    return {"user": claims["email"], "role": claims["role"]}
```

---

## Authorization (RBAC) guidance

`auth_integration` intentionally focuses on **authentication** (who you are).  
Your services should implement **authorization** (what you can do).

Recommended pattern:

- `auth_integration`:
  - validates credentials
  - returns `ClaimsUser`
  - attaches `request.user_claims`

- your service (e.g., `lumen_reports`):
  - defines DRF/FastAPI permission rules:
    - role checks (`technologist` vs `physician`)
    - object-level checks (who can access a specific exam)
    - signing/finalization rules

This keeps the shared library lightweight and avoids coupling it to domain models.

---

## Error behavior

- **No credentials** → returns `None` (request remains anonymous)
- **Invalid / expired token** → raises `AuthenticationFailed` (HTTP 401)
- **Auth API unavailable / misconfigured** → raises HTTP 503

---

## Development

### Local setup
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -e .
```

### Run checks (repo harness)
```bash
python manage.py check
```

---

## Versioning & stability

DRF loads authentication classes by **string import path**.  
To avoid breaking consumers when internal modules move, use the stable entrypoint:

✅ `auth_integration.authentication.ExternalJWTAuthentication`

Internals live under framework folders (e.g., `auth_integration.django.*`, `auth_integration.fastapi.*`)
and may evolve without breaking the public import path.

---

## Maintainer

Maintained by **Anthony Narine**  
© 2025 — Released under the MIT License
