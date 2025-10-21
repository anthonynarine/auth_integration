# 🔄 Tutorial: Updating Backends that Use auth_integration v2.0.0

This guide explains how to update your Django or FastAPI backend
(Lumen Reports, Lumen Media, Dubin, HL7, etc.) after new releases of
the **auth_integration** package.

---

## 🧱 1. Update the Package Version
When a new version of `auth_integration` is released:

Open **pyproject.toml** inside the auth_integration repo:

```toml
[project]
name = "auth_integration"
version = "2.0.0"   # ⬅️ bump this
```

Then tag and push:
```bash
git add .
git commit -m "chore(release): bump version to 2.0.0"
git tag v2.0.0
git push origin main
git push origin v2.0.0
```

✅ GitHub now hosts a tagged build.

---

## ⚙️ 2. Update Each Backend’s `requirements.txt`
Change the version tag for the dependency:

```txt
auth_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/auth_integration.git@v2.0.0
```

💡 Keep `${GITHUB_TOKEN}` in your `.env` or keychain — never commit it.

---

## 🧰 3. Reinstall the Package
In the backend’s virtual environment:
```bash
pip install --upgrade -r requirements.txt
```

Check:
```
Successfully installed auth_integration-2.0.0
```

---

## 🔄 4. Restart the Backend
**For Django:**
```bash
python manage.py runserver
```

**For FastAPI:**
```bash
uvicorn lumen_media.main:app --reload
```

**For Dockerized services:**
```bash
docker-compose build
docker-compose up -d
```

---

## 🧾 5. Verify the Update
```bash
pip show auth_integration
```
Should print:
```
Name: auth_integration
Version: 2.0.0
```

Test a secured API (e.g., `/api/reports/`) and confirm that:
- The service calls `/whoami/` via Gait Auth API.
- No authentication errors occur in logs.

---

## 🔧 6. Recommended Workflows

### Dev Tag Workflow
```bash
git tag -f dev
git push origin dev --force
```
Then in backend:
```txt
auth_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/auth_integration.git@dev
```
→ reinstall when dev changes.

### Release Workflow
Use semantic versioning (`2.0.0`, `2.1.0`, etc.) for production releases.

---

## 🔑 Summary

| Step | Action |
|------|---------|
| 1️⃣ | Bump version + tag release in `auth_integration` |
| 2️⃣ | Update backend’s `requirements.txt` |
| 3️⃣ | Reinstall dependencies |
| 4️⃣ | Restart backend |
| 5️⃣ | Verify with `pip show` or API call |

---

Maintained by **Anthony Narine**  
© 2025 — Auth Integration Project
