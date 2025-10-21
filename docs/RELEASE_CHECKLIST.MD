# 🚀 Release Checklist for auth_integration v2.0.0

This guide explains how to cut a new release of the **auth_integration** package,
publish it to GitHub or a private registry, and make it available for any backend (Lumen Reports, Media, Dubin, etc.).

---

## 🧱 1. Make Code Changes
- Update or fix code inside `auth_integration/`
- Add or update documentation under `/docs/modules/`
- Run unit or integration tests (pytest)

---

## 🧩 2. Bump Version in pyproject.toml
Open **pyproject.toml** and update the version:

```toml
[project]
version = "2.0.0"
```

Use **semantic versioning**:
| Type | Example | Meaning |
|------|----------|----------|
| MAJOR | 2.0.0 | Breaking changes or major new features |
| MINOR | 2.1.0 | Backward‑compatible features |
| PATCH | 2.1.1 | Bug fixes only |

---

## 🧠 3. Commit and Tag the Release
```bash
git add .
git commit -m "chore(release): bump version to 2.0.0"

# Create a Git tag matching the version
git tag v2.0.0
```

---

## ☁️ 4. Push to GitHub
```bash
git push origin main
git push origin v2.0.0
```

Now GitHub holds both the code and the version tag.

---

## ⚙️ 5. Update Backends
Each backend lists this package in its `requirements.txt`:

```txt
auth_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/auth_integration.git@v2.0.0
```

Then reinstall:
```bash
pip install --upgrade -r requirements.txt
```

Restart backend (Django runserver, Daphne, or Docker).

---

## 🧾 6. Verify Installation
```bash
pip show auth_integration
```
→ should show:
```
Name: auth_integration
Version: 2.0.0
```

Run a sample API request (e.g., `/api/templates/carotid/`)  
and confirm `/whoami/` is hit successfully by the backend.

---

## 🧪 7. (Optional) Dev Tag Workflow
For rapid iteration between services:

```bash
git tag -f dev
git push origin dev --force
```

Then in backends:
```txt
auth_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/auth_integration.git@dev
```

Reinstall:
```bash
pip install --upgrade -r requirements.txt
```

---

## ✅ Summary
1. Bump version → Commit → Tag  
2. Push main + tag  
3. Update backend requirements  
4. Reinstall & restart  
5. Verify with `pip show auth_integration`

---

Maintained by **Anthony Narine**  
© 2025 — Auth Integration Project
