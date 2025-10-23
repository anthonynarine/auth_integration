🔐 Auth Integration for Django




gait_integration is a Django package that connects your backend to Gait, a centralized Auth API.
It validates JWTs by calling Gait /api/whoami/ and enforces role-based permissions inside Django.

No more scattered JWT secrets. No more duplicated role logic. Just one source of truth for authentication and identity.

✨ What It Does

🔒 Centralized Auth → All tokens validated by Gait

📥 Token Introspection → Calls /api/whoami/ to fetch user claims

👤 Identity Injection → Attaches claims to request.user_claims

🛡 DRF Permissions → Role checks like HasRole("technologist")

⚡ Extensible → Add caching, group roles, or custom permissions

🔑 End-to-End Flow

React Frontend

User logs in to Gait → receives JWT

Sends API requests to Django with:

Authorization: Bearer <JWT>


Django Backend (with gait_integration)

ExternalJWTAuthentication extracts the JWT

Calls:

GET https://gait.example.com/api/whoami/
Authorization: Bearer <JWT>


Gait (Auth API)

Validates token

Returns claims:

{ "id": "user-123", "email": "tech@example.com", "role": "technologist" }


Django Backend

Attaches claims to request.user_claims

Runs DRF permission checks (e.g. HasRole("technologist"))

Executes the view securely

🖼 Architecture
Mermaid Diagram (renders in GitHub/Notion)
sequenceDiagram
    participant React as React Frontend
    participant Django as Django Backend (gait_integration)
    participant Gait as Gait (Auth API)

    React->>Gait: Login → Get JWT
    Gait-->>React: Return Access Token

    React->>Django: API request (Bearer JWT)
    Django->>Gait: GET /api/whoami/
    Gait-->>Django: User claims {id, email, role}

    Django->>Django: Populate request.user_claims
    Django->>Django: HasRole("technologist")
    Django-->>React: Secure response

ASCII Fallback
+-------------------+                         +--------------------+
|   React Frontend  |                         |        Gait        |
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
|  Django Backend             |-------------->|  /api/whoami/      |
|  (with gait_integration)    |              |  (Validates JWT)   |
|-----------------------------|              +--------------------+
| - ExternalJWTAuthentication |
| - request.user_claims       |
| - HasRole('technologist')   |
+-----------------------------+

⚙️ Setup
1. Install
pip install git+https://<token>@github.com/anthonynarine/gait_integration.git

2. Configure Django
# settings.py
AUTH_API_URL = "https://gait.example.com/api"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "gait_integration.authentication.ExternalJWTAuthentication",
    ]
}

💻 Usage Example
from rest_framework.views import APIView
from rest_framework.response import Response
from gait_integration.permissions import HasRole

class TechOnlyView(APIView):
    permission_classes = [HasRole("technologist")]

    def get(self, request):
        return Response({
            "message": f"Hello, {request.user_claims['email']}!"
        })

📘 Gait API Reference
Required Endpoint
GET /api/whoami/
Authorization: Bearer <token>


200 OK Response

{
  "id": "user-123",
  "email": "user@example.com",
  "role": "admin"
}


401 Unauthorized

Invalid / expired token

✅ Benefits

🔒 Secure by design — Django never stores JWT secrets

🧩 Modular — add to any Django app with DRF

🎯 Single source of truth — roles & identity managed in Gait

⚡ Scalable — perfect for multi-service ecosystems

🛠 Roadmap

🔄 Claim caching (Redis / Django cache)

👥 Group-based permissions (HasAnyRole, IsAdminOrDoctor)

📝 Audit logging for authentication failures

👤 Maintainer

Maintained by Anthony Narine
Originally built for the Lumen vascular reporting platform
Now reusable for any Django project with centralized authentication.

This version is:

Polished + professional for GitHub

Branded with Gait (not just "Auth API")

Detailed in what it does (overview + flow + visuals)

Easy to skim with emojis, badges, and hierarchy

👉 Want me to also create a “Usage in Multi-Service Setup” section (with an example of multiple Django services all talking to Gait) so it really sells the scalability aspect?

You said:
yes!
ChatGPT said:

Perfect 🔥 — adding a multi-service usage section will show that gait_integration isn’t just for Lumen, but scales beautifully when you have multiple Django backends all delegating to Gait. That’s where the “single source of truth” story really shines.

Here’s the expanded README with a dedicated section:

🔐 Auth Integration for Django








gait_integration is a Django package that connects your backend to Gait, a centralized Auth API.
It validates JWTs by calling Gait /api/whoami/ and enforces role-based permissions inside Django.

No more scattered JWT secrets. No more duplicated role logic. Just one source of truth for authentication and identity.

✨ What It Does

🔒 Centralized Auth → All tokens validated by Gait

📥 Token Introspection → Calls /api/whoami/ to fetch user claims

👤 Identity Injection → Attaches claims to request.user_claims

🛡 DRF Permissions → Role checks like HasRole("technologist")

⚡ Extensible → Add caching, group roles, or custom permissions

🔑 End-to-End Flow

React Frontend

User logs in to Gait → receives JWT

Sends API requests to Django with:

Authorization: Bearer <JWT>


Django Backend (with gait_integration)

ExternalJWTAuthentication extracts the JWT

Calls:

GET https://gait.example.com/api/whoami/
Authorization: Bearer <JWT>


Gait (Auth API)

Validates token

Returns claims:

{ "id": "user-123", "email": "tech@example.com", "role": "technologist" }


Django Backend

Attaches claims to request.user_claims

Runs DRF permission checks (e.g. HasRole("technologist"))

Executes the view securely

🖼 Architecture
Mermaid Sequence Diagram
sequenceDiagram
    participant React as React Frontend
    participant Django as Django Backend (gait_integration)
    participant Gait as Gait (Auth API)

    React->>Gait: Login → Get JWT
    Gait-->>React: Return Access Token

    React->>Django: API request (Bearer JWT)
    Django->>Gait: GET /api/whoami/
    Gait-->>Django: User claims {id, email, role}

    Django->>Django: Populate request.user_claims
    Django->>Django: HasRole("technologist")
    Django-->>React: Secure response

⚙️ Setup
1. Install
pip install git+https://<token>@github.com/anthonynarine/gait_integration.git

2. Configure Django
# settings.py
AUTH_API_URL = "https://gait.example.com/api"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "gait_integration.authentication.ExternalJWTAuthentication",
    ]
}

💻 Usage Example
from rest_framework.views import APIView
from rest_framework.response import Response
from gait_integration.permissions import HasRole

class TechOnlyView(APIView):
    permission_classes = [HasRole("technologist")]

    def get(self, request):
        return Response({
            "message": f"Hello, {request.user_claims['email']}!"
        })

🌐 Usage in Multi-Service Setups

One of the biggest advantages of gait_integration is how it scales in a microservices environment.

Imagine you have multiple Django services:

Lumen → handles clinical reporting

Image API → handles ultrasound image storage/retrieval

Billing API → handles insurance claims

Instead of each service handling JWT validation separately:

All services trust Gait for identity.

Each one uses gait_integration to forward tokens to /api/whoami/.

Roles & claims are enforced consistently everywhere.

Multi-Service Flow (Mermaid Diagram)
flowchart LR
    React[React Frontend] -->|Login| Gait[(Gait Auth API)]
    Gait -->|JWT| React

    React -->|Bearer JWT| Lumen[Lumen Django Backend]
    React -->|Bearer JWT| ImageAPI[Image API Backend]
    React -->|Bearer JWT| Billing[Billing API Backend]

    Lumen -->|GET /api/whoami/| Gait
    ImageAPI -->|GET /api/whoami/| Gait
    Billing -->|GET /api/whoami/| Gait

    Gait -->|Claims| Lumen
    Gait -->|Claims| ImageAPI
    Gait -->|Claims| Billing

Why This Matters

🔒 Security → Only Gait knows how to validate tokens

📏 Consistency → Same roles, same claims across all services

⚡ Scalability → Add new services with no extra auth logic

🧩 Flexibility → Permissions live in DRF (HasRole, etc.), identity lives in Gait

📘 Gait API Reference
Required Endpoint
GET /api/whoami/
Authorization: Bearer <token>


200 OK Response

{
  "id": "user-123",
  "email": "user@example.com",
  "role": "admin"
}


401 Unauthorized

Invalid / expired token

✅ Benefits

🔒 Secure by design — Django never stores JWT secrets

🧩 Modular — add to any Django app with DRF

🎯 Single source of truth — roles & identity managed in Gait

⚡ Scalable — perfect for multi-service ecosystems

🛠 Roadmap

🔄 Claim caching (Redis / Django cache)

👥 Group-based permissions (HasAnyRole, IsAdminOrDoctor)

📝 Audit logging for authentication failures

👤 Maintainer

Maintained by Anthony Narine
Originally built for the Lumen vascular reporting platform
Now reusable for any Django project with centralized authentication.