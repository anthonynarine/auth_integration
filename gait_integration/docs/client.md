# ⚙️ Auth Integration — client.py

## Overview
`client.py` is the **core validator** for the Auth Integration package.  
It performs asynchronous JWT validation by calling the `/api/whoami/` endpoint on the **Gait Auth API**.

---

## 🧱 Responsibilities

| Step | Action | Notes |
|------|---------|-------|
| 1️⃣ | Accept a JWT (Bearer token) | From Django or FastAPI |
| 2️⃣ | Call Gait `/whoami/` endpoint | Using `httpx.AsyncClient` |
| 3️⃣ | Return user claims (id, email, role) | JSON response |
| 4️⃣ | Raise structured errors | `InvalidTokenError`, `AuthServiceUnavailable` |

---

## Example Usage

```python
from gait_integration.client import validate_token

claims = await validate_token(token="eyJhbGciOiJI...")
print(claims["role"])  # physician
```

---

Maintained by **Anthony Narine**  
© 2025 — Auth Integration Project
