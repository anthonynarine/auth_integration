# Release Checklist

## 1. Prepare Code
- Ensure all tests pass.
- Update documentation in `/docs` if applicable.
- Increment the version in `pyproject.toml` following semantic versioning.

## 2. Commit and Tag

```bash
git add .
git commit -m "chore(release): bump version to x.y.z"
git tag vX.Y.Z
```

## 3. Push to Remote

```bash
git push origin main
git push origin vX.Y.Z
```

## 4. Create the GitHub Release (do not skip — a tag alone is not enough)

Pushing a tag makes the version pip-installable, but the Releases page on GitHub shows the latest **Release** object (title + notes), which is a separate thing you must create explicitly — otherwise it keeps showing the previous version as "latest" even though the new tag/commit both exist.

```bash
gh release create vX.Y.Z --title "Title: vX.Y.Z" --notes "One-line summary of the fix"
```

Or via the web UI: `github.com/anthonynarine/auth_integration/releases/new`.

## 6. Update Dependent Services

In each dependent backend's `requirements.txt` (this repo is public, so no token is needed in the URL — `lumen_reports` and `lumen_ai/brain/backend` both pin by raw commit hash today, not a tag; either works):

```
auth_integration @ git+https://github.com/anthonynarine/auth_integration.git@vX.Y.Z
```

Then reinstall — **unless** the consumer uses an editable install (`pip show auth_integration` will say "Editable project location: ..."), in which case the fix is already live locally and reinstalling would silently replace the editable install with a pinned one. Check first.

```bash
pip install --upgrade -r requirements.txt
```

## 7. Verify

```bash
pip show auth_integration
```

---

Maintained by **Anthony Narine**  
© 2025
