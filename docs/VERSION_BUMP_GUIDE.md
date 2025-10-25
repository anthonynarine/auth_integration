# 🚀 Version Bumping & Release Guide for `auth_integration`

This guide explains how to use the **`bump_version.sh`** script to update your
package version, commit, tag, and push a new public release to GitHub — all in one command.

---

## 🧠 Overview

The `bump_version.sh` script automates version management for this repository.

It performs the following actions:

1. ✅ Updates the `version` field in **`pyproject.toml`**
2. ✅ Updates version references (like `v0.2.3`) in **`README.md`**
3. ✅ Commits the changes to Git
4. ✅ Creates a new Git **tag** (e.g. `v0.2.4`)
5. ✅ Pushes both the commit and the tag to GitHub
6. ✅ Prints the new `pip install` command for you to use in other projects

This ensures every release is clean, traceable, and installable directly via GitHub.

---

## 📂 Project Structure

You should **run this script only inside the root directory** of this repo,
where your package files are located:

```
auth_integration/
├── pyproject.toml
├── README.md
├── bump_version.sh
├── tests/
└── auth_integration/
```

---

## ⚙️ Usage

### Step 1: Make the script executable (only once)
```bash
chmod +x bump_version.sh
```

### Step 2: Run it with the new version number
```bash
./bump_version.sh 0.2.4
```

That will:
- Update version numbers across files  
- Create a commit with message like  
  `"⬆️ Bump version to 0.2.4"`  
- Create tag `v0.2.4`  
- Push both to GitHub

---

## 🧩 Example Output

```
🚀 Bumping version to 0.2.4...
✏️  Updating pyproject.toml...
✏️  Updating README.md...
📦 Creating git commit and tag...
[main 123abc] ⬆️ Bump version to 0.2.4
 2 files changed, 2 insertions(+), 2 deletions(-)
✅ Version bumped to 0.2.4 and pushed to GitHub.
🎉 Install command:
    pip install git+https://github.com/anthonynarine/auth_integration.git@v0.2.4
```

---

## 🧱 Verify the Update

After running the script, confirm the version bump worked:

```bash
grep version pyproject.toml
git tag --sort=-v:refname | head -3
```

Then push tags if needed:
```bash
git push origin --tags
```

Check your tags here:  
👉 [https://github.com/anthonynarine/auth_integration/tags](https://github.com/anthonynarine/auth_integration/tags)

---

## 🧪 Verify Installation

You can install the latest version anywhere with:

```bash
pip install git+https://github.com/anthonynarine/auth_integration.git@v0.2.4
```

Then confirm:
```bash
python -c "from auth_integration.client import validate_token; print('✅ import OK')"
```

---

## 💡 Notes

- Always run the script from inside the `auth_integration/` directory  
  (the one that contains `pyproject.toml`).
- The script supports both macOS and Windows (Git Bash).
- Old versions remain available via tags for reproducible installs.

---

## 🏁 Summary

| Step | Command | Description |
|------|----------|-------------|
| Make executable | `chmod +x bump_version.sh` | One-time setup |
| Bump version | `./bump_version.sh 0.2.4` | Updates + tags new release |
| Verify | `git tag`, `grep version pyproject.toml` | Check new version |
| Push manually (if needed) | `git push origin v0.2.4` | Sync tag to GitHub |
| Install elsewhere | `pip install git+https://github.com/anthonynarine/auth_integration.git@v0.2.4` | Use in other projects |

---

Maintained by **Anthony Narine**  
© 2025 — Part of the **Lumen** ecosystem 🩺💡
