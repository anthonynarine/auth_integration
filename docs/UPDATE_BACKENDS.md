# Updating Dependent Backends

## Overview
This document describes how to update Django, FastAPI, or Dockerized backends
that depend on the `auth_integration` package after a new release.

## Steps

1. Update the version tag in `requirements.txt` or `pyproject.toml`.
2. Reinstall dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```
3. Restart the backend service:
   - Django: `python manage.py runserver`
   - FastAPI: `uvicorn app.main:app --reload`
   - Docker: `docker compose build && docker compose up -d`
4. Verify the installed version with:
   ```bash
   pip show auth_integration
   ```

## Notes
- Always use semantic versioning for production releases.
- Do not commit authentication tokens or credentials.

Maintained by **Anthony Narine**, 2025
