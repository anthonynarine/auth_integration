🚀 Release Checklist for auth_integration

This guide explains how to cut a new release of the auth_integration package, publish it to GitHub, and make it available for backends like Lumen.

1. Make Your Code Changes

Update or fix code inside auth_integration/.

Add/update tests if needed.

Update docs (docs/UPDATE_AUTH_INTEGRATION.md, etc.) if workflows have changed.

2. Bump Version in pyproject.toml

Open pyproject.toml and update the version:

[project]
version = "0.3.0"   # ⬅️ bump this


Use semantic versioning:

MAJOR.MINOR.PATCH

0.3.0 → new features

0.3.1 → bug fixes only

3. Commit and Tag the Release
git add .
git commit -m "chore(release): bump version to 0.3.0"

# Create a Git tag matching the version
git tag v0.3.0

4. Push to GitHub
git push origin main
git push origin v0.3.0


Now GitHub has both the code and the version tag.

5. Update Backends

In Lumen (or any backend), update requirements.txt:

auth_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/auth_integration.git@v0.3.0


Reinstall:

pip install --upgrade -r requirements.txt


Restart backend (Django runserver, Daphne, or Docker).

6. Verify

Check installed version:

pip show auth_integration


→ should show Version: 0.3.0

Run a test request (/api/templates/carotid/) and confirm auth flow works (calls /whoami/).

7. (Optional) Dev Tag Workflow

For fast iteration, use a moving dev tag:

git tag -f dev
git push origin dev --force


Then in backends:

auth_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/auth_integration.git@dev


Reinstall with:

pip install --upgrade -r requirements.txt


✅ That’s it — package is versioned, published, and ready for backends to consume.

Now your docs folder will look like this:

auth_integration/
  ├── docs/
  │    ├── UPDATE_AUTH_INTEGRATION.md   # backend update guide
  │    └── RELEASE_CHECKLIST.md         # package release guide
