# Updating Dependent Backends

## Overview
This document describes how to update Django, FastAPI, or Dockerized backends
that depend on the `auth_integration` package after a new release.

**Known current consumers**: `lumen_reports` (`requirements.txt`) and `lumen_ai/brain/backend` (`requirements.txt`) — both pin by commit hash. `lumen_media` does **not** depend on this package (separate hand-written FastAPI adapter) — don't try to update it here.

## First: check whether this consumer uses an editable install

```bash
pip show auth_integration
```

If it says `Editable project location: ...` pointing at this repo's local path, **the fix is already live** for that consumer the moment it's saved to disk — that's how local dev is set up for both `lumen_reports` and `lumen_ai`. Running `pip install --upgrade -r requirements.txt` in that case would *replace* the convenient editable install with a pinned, non-editable one — only do this deliberately, not by habit.

For anywhere else (a fresh machine, CI, production) — that's a real pinned install, and the steps below apply normally.

## Steps

1. Update the pinned commit hash or tag in `requirements.txt`:
   ```
   auth_integration @ git+https://github.com/anthonynarine/auth_integration.git@<new commit or vX.Y.Z>
   ```
   Note: some of this project's `requirements.txt` files are **UTF-16 encoded** (check with `file requirements.txt` before editing with a plain text tool — a naive UTF-8 edit will corrupt them). Safe approach:
   ```python
   with open('requirements.txt', encoding='utf-16') as f:
       content = f.read()
   content = content.replace(old_hash, new_hash)
   with open('requirements.txt', 'w', encoding='utf-16') as f:
       f.write(content)
   ```
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
- Before assuming a fix in this package reaches a given service, confirm that service actually imports `auth_integration` (`grep -rn "auth_integration" <service>/`) rather than having its own separate implementation.

Maintained by **Anthony Narine**, 2025
