# auth_integration

A reusable Django package for integrating with a centralized Auth API using JWT authentication.

This package allows any Django app (e.g., Lumen) to:

- ✅ Authenticate users via JWT (access or refresh token)
- ✅ Support both `HS256` and `RS256` token verification
- ✅ Enforce role-based access (e.g. "doctor", "technologist")
- ✅ Optionally publish user-related events via RabbitMQ
- ✅ Avoid the need for a local user model or login system

---

## Features

- JWT Middleware (cookie or Authorization header)
- DRF permission classes (`IsAuthenticated`, `IsDoctor`, etc.)
- Role-based decorators
- RabbitMQ pub/sub utilities
- Clean environment-based config (`.env`)
- Modular and testable

---

## Installation

Clone or add to your project as a pip dependency:

```bash
pip install git+https://github.com/YOUR-ORG/auth_integration.git@main
