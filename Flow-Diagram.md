sequenceDiagram
    autonumber
    actor Tech as Technologist (Frontend)
    participant UI as React (CarotidExamPage + Formik)
    participant API as Axios (carotidAPI/examApi)
    participant DRF as Lumen Reports API (DRF Views)
    participant AUTH as ExternalJWTAuthentication (auth_integration)
    participant GAIT as Gait Auth API (/whoami/)
    participant DB as Postgres (Exam/Segment/Measurement)
    participant CALC as Carotid Calculators
    participant CONC as Conclusion Service/Builder

    Note over Tech,UI: Template already loads & renders worksheet UI
    Tech->>UI: Open Carotid Exam Page
    UI->>API: GET /api/templates/carotid/?site=mount_sinai_hospital
    API->>DRF: GET templates endpoint
    DRF-->>API: 200 Template JSON
    API-->>UI: Template JSON
    UI-->>Tech: Worksheet rendered (segments + inputs)
