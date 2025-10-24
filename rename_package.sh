#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────────────
#  Project-Wide Rename Script — auth_integration → auth_integration
#  Scoped for AUTH_INTEGRATION/ project root
#  Works on Git Bash (Windows) and macOS/Linux
#
#  Usage:
#    ./rename_back_to_auth.sh
# ──────────────────────────────────────────────────────────────

OLD_NAME="auth_integration"
NEW_NAME="auth_integration"

echo "🚀 Starting full project rename: ${OLD_NAME} → ${NEW_NAME}"

# --- Cross-platform sed -i handling ------------------------------------------
SED_INPLACE=()
if sed --version >/dev/null 2>&1; then
  SED_INPLACE=(-i)
else
  SED_INPLACE=(-i '')
fi

# --- Find and replace across project -----------------------------------------
echo "🧭 Scanning for ${OLD_NAME} references..."
MATCHES=$(grep -RIn "${OLD_NAME}" . \
  --exclude-dir=".git" \
  --exclude-dir="gait_int_venv" \
  --exclude-dir=".pytest_cache" \
  --exclude-dir="__pycache__" \
  --exclude-dir="node_modules" \
  --exclude-dir="dist" \
  || true)

if [[ -z "$MATCHES" ]]; then
  echo "✅ No references to ${OLD_NAME} found."
else
  echo "🔍 Found references — updating..."
  find . -type f \
    ! -path "./.git/*" \
    ! -path "./gait_int_venv/*" \
    ! -path "./.pytest_cache/*" \
    ! -path "./__pycache__/*" \
    ! -path "./node_modules/*" \
    ! -path "./dist/*" \
    -exec sed "${SED_INPLACE[@]}" "s/${OLD_NAME}/${NEW_NAME}/g" {} +
  echo "✅ Text replacements complete."
fi

# --- Remove old build artifacts ----------------------------------------------
if [[ -d "${OLD_NAME}.egg-info" ]]; then
  echo "🧹 Removing old ${OLD_NAME}.egg-info directory..."
  rm -rf "${OLD_NAME}.egg-info"
  echo "✅ Removed."
fi

# --- Reinstall package in editable mode --------------------------------------
echo "📦 Reinstalling package in editable mode..."
if python -m pip install -e . >/dev/null 2>&1; then
  echo "✅ Editable install complete."
else
  echo "⚠️  pip install -e . failed — please check setup.py or pyproject.toml"
fi

# --- Verify import -----------------------------------------------------------
echo "🧪 Verifying import: from ${NEW_NAME}.client import validate_token"
python - <<PYCODE
try:
    from ${NEW_NAME}.client import validate_token  # type: ignore
    print("✅ Import OK — ${NEW_NAME} is ready to use.")
except Exception as e:
    print("❌ Import failed:", e)
    raise SystemExit(1)
PYCODE

echo "🎉 Done! All references updated and package reinstalled successfully."
