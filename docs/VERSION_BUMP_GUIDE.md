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

## ⚠️ The step this script does NOT do: creating a GitHub Release

`bump_version.sh` pushes a git **tag**. That's enough to make `pip install ...@vX.Y.Z` work — but it does **not** create a GitHub **Release** (title + changelog body), which is a separate GitHub feature. Every version from `v0.3.2` onward has a real Release object, and the Releases page shows whatever the latest *Release* is, not the latest *tag*. Skip this step and the Releases page will keep showing the previous version as "latest" even though the new tag and commit both exist and work fine for installs.

After running the script, also do one of:

```bash
# Via gh CLI, if installed:
gh release create vX.Y.Z --title "Title: vX.Y.Z" --notes "One-line summary of the fix"

# Or via the web UI:
# github.com/anthonynarine/auth_integration/releases/new
#   Tag: vX.Y.Z | Title: "Title: vX.Y.Z" | Body: the fix commit's summary line
```

---

## 🏁 Summary

| Step | Command | Description |
|------|----------|-------------|
| Make executable | `chmod +x bump_version.sh` | One-time setup |
| Bump version | `./bump_version.sh 0.2.4` | Updates + tags new release |
| Verify | `git tag`, `grep version pyproject.toml` | Check new version |
| Push manually (if needed) | `git push origin v0.2.4` | Sync tag to GitHub |
| **Create the GitHub Release** | `gh release create v0.2.4 ...` or the web UI | **Not done by the script** — do this or the Releases page won't update |
| Install elsewhere | `pip install git+https://github.com/anthonynarine/auth_integration.git@v0.2.4` | Use in other projects |

---

Maintained by **Anthony Narine**  
© 2025 — Part of the **Lumen** ecosystem 🩺💡
