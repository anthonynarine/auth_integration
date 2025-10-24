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

## 4. Update Dependent Services

In dependent backends:

```
gait_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/gait_integration.git@vX.Y.Z
```

Then reinstall dependencies.

## 5. Verify

```bash
pip show gait_integration
```

---

Maintained by **Anthony Narine**  
© 2025
