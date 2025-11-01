#!/usr/bin/env bash

# to run  cd /path/to/auth_integration
# ./bump_version.sh

set -euo pipefail

NEW_VERSION=${1:-}

if [[ -z "$NEW_VERSION" ]]; then
  echo "❌ Usage: $0 <new_version> (e.g., ./bump_version.sh 0.2.3)"
  exit 1
fi

echo "🚀 Bumping version to $NEW_VERSION..."

# Detect GNU vs BSD sed
SED_INPLACE=()
if sed --version >/dev/null 2>&1; then
  SED_INPLACE=(-i)
else
  SED_INPLACE=(-i '')
fi

# 1️⃣ Update version in pyproject.toml
if grep -qE '^version\s*=' pyproject.toml; then
  echo "✏️  Updating pyproject.toml..."
  sed "${SED_INPLACE[@]}" "s/^version\s*=.*/version = \"${NEW_VERSION}\"/" pyproject.toml
else
  echo "⚠️  Could not find version in pyproject.toml"
fi

# 2️⃣ Update README.md
if [[ -f README.md ]]; then
  echo "✏️  Updating README.md..."
  sed "${SED_INPLACE[@]}" "s/v[0-9]\+\.[0-9]\+\.[0-9]\+/v${NEW_VERSION}/g" README.md
  sed "${SED_INPLACE[@]}" "s/[0-9]\+\.[0-9]\+\.[0-9]\+/${NEW_VERSION}/g" README.md
else
  echo "⚠️  README.md not found"
fi

# 3️⃣ Commit and tag
echo "📦 Creating git commit and tag..."
git add pyproject.toml README.md || true
git commit -m "⬆️ Bump version to ${NEW_VERSION}" || echo "ℹ️  Nothing to commit."
git tag -a "v${NEW_VERSION}" -m "Release v${NEW_VERSION}"
git push
git push origin "v${NEW_VERSION}"

echo "✅ Version bumped to ${NEW_VERSION} and pushed to GitHub."
echo "🎉 Install command:"
echo "    pip install git+https://github.com/anthonynarine/auth_integration.git@v${NEW_VERSION}"
