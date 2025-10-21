# 🧩 Auth Integration — Module Overview

## Overview
The **Auth Integration** package provides a unified authentication system for Django and FastAPI services that connect to the **Gait Auth API**.

It validates JWTs, extracts user claims, and enforces role-based permissions across all Lumen microservices (Reports, Media, Dubin, HL7, etc.).

---

## 🧠 Architecture Diagram

```mermaid
flowchart TD
    subgraph Core["Core Package"]
        A[client.py] --> B[exceptions.py]
        A --> C[utils.py]
        D[permissions.py] --> C
    end

    subgraph Django["Django Adapter"]
        E[django/authentication.py]
    end

    subgraph FastAPI["FastAPI Adapter"]
        F[fastapi/dependencies.py]
    end

    E --> A
    F --> A
    E --> D
```

---

## 📘 Module Responsibilities

| Module | Role | Used By |
|---------|------|---------|
| `client.py` | Async JWT validator calling Gait `/whoami/` | Django & FastAPI |
| `exceptions.py` | Central exception classes for validation errors | All |
| `permissions.py` | Role-based DRF permission classes | Django |
| `utils.py` | Helper utilities for claims & roles | All |
| `django/authentication.py` | Authentication backend for DRF | Django |
| `fastapi/dependencies.py` | Async dependency for route protection | FastAPI |

---

## 🧩 Token Lifecycle

```mermaid
sequenceDiagram
    participant FE as React Frontend
    participant BE as Backend (Django/FastAPI)
    participant GA as Gait Auth API

    FE->>GA: Login → /api/login/
    GA-->>FE: JWT Access Token
    FE->>BE: Request with Bearer Token
    BE->>client.py: validate_token(token)
    client.py->>GA: GET /api/whoami/
    GA-->>client.py: 200 OK (User Claims)
    client.py-->>BE: Return validated claims
    BE-->>FE: Secure Response (user data)
```

---

Maintained by **Anthony Narine**  
© 2025 — Auth Integration Project
