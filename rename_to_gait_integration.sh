#!/usr/bin/env bash
set -e

echo "🚀 Starting rename: gait_integration → gait_integration"

# Step 1: Rename directory
if [ -d "gait_integration" ]; then
  mv gait_integration gait_integration
  echo "✅ Renamed folder to gait_integration/"
else
  echo "❌ Folder 'gait_integration' not found."
  exit 1
fi

# Step 2: Replace imports across all files
echo "🔍 Updating imports..."
grep -rl "gait_integration" . --exclude-dir=.git | xargs sed -i 's/gait_integration/gait_integration/g'
echo "✅ Imports updated."

# Step 3: Update pyproject.toml
if [ -f "pyproject.toml" ]; then
  sed -i 's/name = "auth-integration"/name = "gait-integration"/' pyproject.toml
  sed -i 's/packages = \["gait_integration"\]/packages = ["gait_integration"]/' pyproject.toml
  echo "✅ pyproject.toml updated."
else
  echo "⚠️ pyproject.toml not found, skipping."
fi

# Step 4: Rebuild the package
echo "📦 Rebuilding package..."
pip uninstall -y auth-integration || true
pip install -e .
echo "✅ Package rebuilt."

# Step 5: Verify import
echo "🧠 Testing import..."
python - <<'EOF'
try:
    from gait_integration.client import validate_token
    print("🎉 Import test passed! gait_integration is ready.")
except Exception as e:
    print("❌ Import test failed:", e)
EOF

echo "✨ Rename completed successfully."
