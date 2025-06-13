# 🔐 Auth Integration Package for Django (auth_integration)

This private package allows Django backends like **Lumen** to securely authenticate users using a centralized **Auth API**. It verifies JWTs, fetches user claims from the `/api/me/` endpoint, and integrates with Django REST Framework’s authentication and permission system.

> Built for secure, scalable multi-service apps using React frontends, Django backends, and a centralized authentication server.

---

## 🚀 What It Does

- Verifies JWTs by calling your **Auth API**'s `/api/me/` endpoint
- Attaches user claims (id, email, role, etc.) to `request.user_claims`
- Provides DRF-compatible authentication and permission classes
- Optionally caches claims for performance
- Keeps all user identity and role logic **centralized**

---

## 🧠 Flow Model

```text
[ React Frontend ]
    |
    | 1. Login → receives access token
    |
    | 2. Makes request to Lumen with:
    |    Authorization: Bearer <JWT>
    |
    v
[ Lumen (Django Backend) ]
    |
    | 3. Calls auth_integration.AuthAPITokenAuthentication
    | 4. Makes request to:
    |    GET https://auth.example.com/api/me/
    |    with same Authorization header
    |
    v
[ Auth API ]
    |
    | 5. Validates token
    |    Returns user info:
    |    {
    |      "id": "user-123",
    |      "email": "tech@example.com",
    |      "role": "rvt"
    |    }
    |
    v
[ Lumen ]
    |
    | 6. request.user_claims is populated
    | 7. DRF permission checks like HasRole("rvt")
    |
    v
[ View executes securely ]
📦 Installation
Option 1: Install via Git (recommended for private use)
bash
Copy
Edit
pip install git+https://github.com/YOUR_USERNAME/auth_integration.git@main
Option 2: Install locally (during development)
bash
Copy
Edit
pip install -e /path/to/auth_integration
⚙️ Configuration in Django (Lumen)
Step 1: Add to INSTALLED_APPS if needed (optional for packaging)
python
Copy
Edit
INSTALLED_APPS = [
    ...
    'auth_integration',
]
Step 2: Configure REST Framework
python
Copy
Edit
# settings.py

AUTH_API_URL = "https://auth.example.com"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "auth_integration.authentication.AuthAPITokenAuthentication",
    ],
}
🔐 Usage in Views
Add Role-Based Permissions
python
Copy
Edit
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_integration.permissions import HasRole

class TechOnlyView(APIView):
    permission_classes = [HasRole("rvt")]

    def get(self, request):
        return Response({"message": f"Hello, {request.user_claims['email']}!"})
🛠 Authentication Class
AuthAPITokenAuthentication
Extracts JWT from Authorization header

Makes a secure HTTP request to your Auth API’s /api/me/

Validates the token and returns user info

Populates request.user_claims with:

json
Copy
Edit
{
  "id": "user-123",
  "email": "tech@example.com",
  "role": "rvt"
}
📘 /api/me/ Endpoint (Auth API)
This must be available at your Auth API:

http
Copy
Edit
GET /api/me/
Authorization: Bearer <token>
Response if valid:
json
Copy
Edit
{
  "id": "user-123",
  "email": "user@example.com",
  "role": "admin"
}
If token is expired or invalid, return 401 Unauthorized.

🔄 Diagram (ASCII-Style Architecture)
plaintext
Copy
Edit
+-------------------+                         +--------------------+
|   React Frontend  |                         |     Auth API       |
|-------------------|                         |--------------------|
| - Login form      |                         | - /api/token/      |
| - Access token    |-----------------------> | - /api/me/         |
| - Sends API call  |                         +--------------------+
|   with JWT        |                                    ▲
+--------|----------+                                    |
         |                                               |
         |  GET /api/... with JWT in header              |
         v                                               |
+-----------------------------+     calls     +--------------------+
|       Lumen Backend         |-------------->|   /api/me/         |
|  (Django + auth_integration)|              |  (Validates JWT)   |
|-----------------------------|              +--------------------+
| - AuthAPITokenAuthentication|
| - request.user_claims       |
| - HasRole("rvt")            |
+-----------------------------+


✅ Advantages
🔒 Secure by design: no JWT secrets stored in Lumen

🧩 Modular: use in any Django app that needs authentication

🛠 Maintains a single source of truth for user identity

💡 Easy to test and extend (add caching, logging, etc.)

🧪 Coming Soon (Optional Features)
Caching of user claims (Redis or Django cache)

CacheUserClaimsMiddleware

Group-based permissions (HasAnyRole, IsAdminOrDoctor)

Audit logging of auth failures

🧑‍💻 Author
Built for the Lumen vascular reporting platform and private clinical tools.
Maintained by Anthony Narine.








