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

    Note over Tech,UI: Create Exam (first persistence step)

    Tech->>UI: Click "Create Exam"
    UI->>API: POST /api/reports/carotid/ (patient + exam metadata)
    API->>DRF: POST create exam request

    Note over DRF,AUTH: DRF Authentication runs before the view
    DRF->>AUTH: authenticate(request)

    alt DEV Bearer Mode
        AUTH->>AUTH: Extract Authorization: Bearer <token>
        AUTH->>GAIT: /whoami/ (validate token)
        GAIT-->>AUTH: 200 Claims JSON
    else PROD Cookie Mode
        AUTH->>AUTH: No Bearer, forward HttpOnly cookies
        AUTH->>GAIT: /whoami/ (validate cookies)
        GAIT-->>AUTH: 200 Claims JSON
    end

    Note over AUTH: ✅ Fix: return ClaimsUser(is_authenticated=True)\n+ attach request.user_claims
    AUTH-->>DRF: (ClaimsUser, token|None)

    alt Auth OK
        DRF->>DB: Create Exam + Segments + Measurements
        DB-->>DRF: Exam created (id, segments, measurements)
        DRF-->>API: 201 { message, exam }
        API-->>UI: exam.id returned
        UI-->>Tech: "Exam Created" + navigates/stores examId
    else Invalid Credentials
        AUTH-->>DRF: raise AuthenticationFailed
        DRF-->>API: 401 Unauthorized
        API-->>UI: show auth error
    else Auth Service Down
        AUTH-->>DRF: raise 503 ServiceUnavailable
        DRF-->>API: 503 Service Unavailable
        API-->>UI: show downtime error
    end

    Note over Tech,UI: Save Segment Measurements (PATCH)

    Tech->>UI: Enter PSV/EDV + plaque fields
    UI->>UI: Formik values updated
    UI->>API: PATCH /api/reports/carotid/{examId}/segments/
    Note over UI: normalizeCarotidFormikToPayload(values)\n=> { segment_name: {psv,edv,...}, ... }
    API->>DRF: PATCH segments payload
    DRF->>AUTH: authenticate(request)
    AUTH->>GAIT: /whoami/ (or cache)
    GAIT-->>AUTH: 200 Claims
    AUTH-->>DRF: (ClaimsUser, token|None)

    DRF->>DB: Update Measurements per segment_name
    DB-->>DRF: Updated rows
    DRF-->>API: 200 { segments_updated: N }
    API-->>UI: Save success
    UI-->>Tech: "Saved"

    Note over Tech,UI: Calculate (derived metrics)

    Tech->>UI: Click "Calculate" (or auto after save)
    UI->>API: POST /api/reports/carotid/{examId}/calculate/
    API->>DRF: Calculate request
    DRF->>AUTH: authenticate(request)
    AUTH->>GAIT: /whoami/ (or cache)
    GAIT-->>AUTH: 200 Claims
    AUTH-->>DRF: (ClaimsUser, token|None)

    DRF->>CALC: Run ICA/CCA ratio + stenosis rules
    CALC->>DB: Persist derived fields (if stored) or compute response
    DB-->>CALC: Segment + measurement data
    CALC-->>DRF: Calculated exam snapshot
    DRF-->>API: 200 Exam serialized
    API-->>UI: Update UI with calculated fields
    UI-->>Tech: Results displayed

    Note over Tech,UI: Conclusion

    UI->>API: GET /api/reports/carotid/{examId}/conclusion/
    API->>DRF: Conclusion request
    DRF->>AUTH: authenticate(request)
    AUTH->>GAIT: /whoami/ (or cache)
    GAIT-->>AUTH: 200 Claims
    AUTH-->>DRF: (ClaimsUser, token|None)

    DRF->>CONC: Build findings + impression text
    CONC-->>DRF: Conclusion JSON
    DRF-->>API: 200 { conclusion }
    API-->>UI: Render conclusion (editable)
    UI-->>Tech: Final narrative visible

    Note over Tech,UI: Reload / Persistence Check (Smoke Test proof)

    Tech->>UI: Refresh page / reopen exam
    UI->>API: GET /api/reports/carotid/{examId}/ (recommended endpoint)
    API->>DRF: Fetch exam detail
    DRF->>AUTH: authenticate(request)
    AUTH->>GAIT: /whoami/ (or cache)
    GAIT-->>AUTH: 200 Claims
    AUTH-->>DRF: (ClaimsUser, token|None)

    DRF->>DB: Load Exam + Segments + Measurements
    DB-->>DRF: Persisted values
    DRF-->>API: 200 Exam JSON
    API-->>UI: normalizeCarotidExamToFormik(exam)
    UI-->>Tech: Values rehydrated (proof of save)
