🔑 How It’s Meant to Be Used

The auth_integration package is designed to let any Django backend securely delegate authentication to a centralized Auth API. Instead of validating JWTs locally, your backend simply forwards them to the Auth API’s /api/whoami/ endpoint for verification. This keeps identity and role management in one place.

End-to-End Flow

React Frontend

User logs in via the Auth API login flow and receives a JWT access token.

All subsequent API calls to your Django service include:

Authorization: Bearer <JWT>


Django Backend (with auth_integration, example Lumen)

Requests hit Django REST Framework views.

ExternalJWTAuthentication extracts the JWT.

A secure call is made to your centralized Auth API (Gait):

GET /api/whoami/
Authorization: Bearer <JWT>


Auth API

Validates the JWT.

Returns user claims, for example:

{
  "id": "user-123",
  "email": "tech@example.com",
  "role": "technologist"
}


Django Backend

Attaches claims to request.user_claims.

Applies DRF permission classes (e.g., HasRole("technologist")).

Executes the view securely if permissions pass.

Why This Matters

🔒 Security: Django services never need to store or manage JWT secrets.

🧩 Scalability: All microservices authenticate consistently against the same Auth API.

🎯 Clarity: Roles and claims are always centralized, easy to update, and enforced uniformly.

That way, the README tells the story of how any service should use the package — not just Lumen — and clarifies that the canonical endpoint is /api/whoami/.

👉 Do you want me to also re-draw the ASCII diagram to match this (with /api/whoami/ instead of /api/me/, and without naming Lumen), so you’ve got both prose + visuals aligned?

You said:
i love the current readme but i think you can imporve it whit your how it' meant to be used and end to end flow 
ChatGPT said:

Perfect ✅ — we’ll keep the structure and style of your current README (which is already really solid), but refine it by folding in my “How it’s Meant to Be Used” + “End-to-End Flow” section. That way the doc feels less Lumen-specific and more like a polished, reusable package README.

Here’s the improved version with everything merged:

🔐 Auth Integration Package for Django (auth_integration)
Building Centralized Authentication with Token Introspection

This private package allows Django backends to securely authenticate users using a centralized Auth API. It verifies JWTs, fetches user claims from the /api/whoami/ endpoint, and integrates with Django REST Framework’s authentication and permission system.

Built for secure, scalable multi-service apps using React frontends, Django backends, and a centralized authentication server.

🔑 How It’s Meant to Be Used

Instead of each Django service validating JWTs locally, auth_integration pushes all responsibility to your Auth API.

Your frontend gets a JWT from the Auth API during login.

Every request to your Django backend includes this JWT.

The backend calls the Auth API’s /api/whoami/ endpoint to validate the token and retrieve user claims.

Those claims are attached to request.user_claims and enforced through DRF permission classes.

This keeps identity, roles, and authorization logic centralized and consistent across all services.

🚀 End-to-End Flow

React Frontend

User logs in and receives a JWT access token.

Sends API calls to Django with:

Authorization: Bearer <JWT>


Django Backend (with auth_integration)

Requests are intercepted by ExternalJWTAuthentication.

It extracts the JWT and makes a secure call to:

GET /api/whoami/
Authorization: Bearer <JWT>


Auth API

Validates the JWT.

Returns user claims:

{
  "id": "user-123",
  "email": "tech@example.com",
  "role": "technologist"
}


Django Backend

Attaches claims to request.user_claims.

DRF permission checks like HasRole("technologist") run.

If checks pass → the view executes securely.

📦 Installation
Option 1: Install via GitHub (recommended for private use)
pip install git+https://<your-personal-access-token>@github.com/anthonynarine/auth_integration.git

Option 2: Install locally during development
pip install -e /path/to/auth_integration

⚙️ Configuration in Django
Step 1: (Optional) Add to INSTALLED_APPS if packaging requires it
INSTALLED_APPS = [
    ...
    'auth_integration',
]

Step 2: Configure Django REST Framework
# settings.py

AUTH_API_URL = "https://auth.example.com/api"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "auth_integration.authentication.ExternalJWTAuthentication",
    ]
}

🔐 Usage in Views
Add Role-Based Permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_integration.permissions import HasRole

class TechOnlyView(APIView):
    permission_classes = [HasRole("technologist")]

    def get(self, request):
        return Response({"message": f"Hello, {request.user_claims['email']}!"})

🛠 Authentication Class
ExternalJWTAuthentication

Extracts JWT from the Authorization header

Sends a secure request to your Auth API’s /api/whoami/ endpoint

Validates the token and returns user info

Populates request.user_claims with:

{
  "id": "user-123",
  "email": "tech@example.com",
  "role": "technologist"
}

📘 Required /api/whoami/ Endpoint (Auth API)
GET /api/whoami/
Authorization: Bearer <token>

Successful Response (200 OK)
{
  "id": "user-123",
  "email": "user@example.com",
  "role": "admin"
}

Invalid Token → 401 Unauthorized
🔄 ASCII Architecture Diagram
+-------------------+                         +--------------------+
|   React Frontend  |                         |     Auth API       |
|-------------------|                         |--------------------|
| - Login form      |                         | - /api/token/      |
| - Access token    |-----------------------> | - /api/whoami/     |
| - Sends API call  |                         +--------------------+
|   with JWT        |                                    ▲
+--------|----------+                                    |
         |                                               |
         |  GET /api/... with JWT in header              |
         v                                               |
+-----------------------------+     calls     +--------------------+
|  Django Backend             |-------------->|   /api/whoami/     |
|  (with auth_integration)    |              |  (Validates JWT)   |
|-----------------------------|              +--------------------+
| - ExternalJWTAuthentication |
| - request.user_claims       |
| - HasRole('technologist')   |
+-----------------------------+

✅ Advantages

🔒 Secure by design: no JWT secrets stored in Django

🧩 Modular: works with any Django app that needs authentication

🎯 Single source of truth for user identity and roles

🛠 Extensible: add caching, logging, or custom permissions

🧪 Coming Soon (Optional Features)

Caching of user claims (Redis or Django cache)

CacheUserClaimsMiddleware

Group-based permissions (HasAnyRole, IsAdminOrDoctor)

Audit logging of auth failures

👤 Author

Maintained by Anthony Narine.
Built originally for the Lumen vascular reporting platform, now reusable in any Django project.