```mermaid
graph LR
  classDef fe fill:#00c853,stroke:#0e6,stroke-width:1.5,color:#fff;
  classDef dj fill:#2962ff,stroke:#1740a0,stroke-width:1.5,color:#fff;
  classDef fa fill:#ffd600,stroke:#c4a000,stroke-width:1.5,color:#000;
  classDef infra fill:#e53935,stroke:#b71c1c,stroke-width:1.5,color:#fff;
  classDef ext fill:#616161,stroke:#424242,color:#fff;

  FE["🟢 React + TS Frontend (lumen_ui)<br/>(Axios, Formik, Tailwind, RAG Drawer)"]:::fe
  Lumen["🟦 lumen_reports (Django Backend)<br/>Templates, Calculators, PDF, HL7"]:::dj
  Gait["🟦 Gait Auth Service (Django)<br/>Internal JWT, Roles, 2FA Security Layer"]:::dj
  AI["🟨 lumen_ai (AI Microservice) (FastAPI)<br/>LangChain RAG — Julia, Kadian, Smith"]:::fa
  Media["🟨 lumen_media (Image Storage API) (FastAPI)<br/>Image/Cine Upload + S3 Storage"]:::fa
  HL7["🟨 HL7 Listener (FastAPI Microservice) (FastAPI)<br/>ORM/ORU Integration"]:::fa
  EMR["🏥 EMR (Epic/NextGen)"]:::ext
  S3["🟥 MinIO/S3 Object Store"]:::infra
  PG["🟥 PostgreSQL"]:::infra
  Redis["🟥 Redis"]:::infra
  Reverse["🟥 Nginx/Traefik Reverse Proxy"]:::infra

  FE--HTTPS-->Reverse
  Reverse-->Lumen
  Reverse-->Media
  Reverse-->AI
  Reverse-->HL7
  Reverse-->Gait
  FE--Auth/Login-->Gait
  Lumen--JWT Validation-->Gait
  Lumen--AI Queries-->AI
  Lumen--Image Links-->Media
  Lumen--HL7 ORU Results-->HL7
  HL7--ORM/ORU-->EMR
  Lumen---PG
  Lumen---Redis
  Media--Stores-->S3
  AI---Redis



sequenceDiagram
  autonumber
  actor Tech as Technologist
  participant UI as React UI
  participant API as Axios API
  participant DRF as Lumen Reports
  participant AUTH as auth_integration
  participant GAIT as Gait /whoami
  participant DB as Postgres
  participant CALC as Calculators
  participant CONC as Conclusion Builder

  Note over Tech,UI: Template loads & renders worksheet UI

  Tech->>UI: Open Carotid Exam Page
  UI->>API: GET template
  API->>DRF: GET /api/templates/carotid
  DRF-->>API: 200 template JSON
  API-->>UI: template JSON

  Tech->>UI: Click Create Exam
  UI->>API: POST create exam
  API->>DRF: POST /api/reports/carotid
  DRF->>AUTH: authenticate(request)
  AUTH->>GAIT: GET /whoami
  GAIT-->>AUTH: 200 claims
  AUTH-->>DRF: ClaimsUser + request.user_claims
  DRF->>DB: Create Exam + Segments + Measurements
  DB-->>DRF: exam created
  DRF-->>API: 201 exam JSON
  API-->>UI: examId stored


```