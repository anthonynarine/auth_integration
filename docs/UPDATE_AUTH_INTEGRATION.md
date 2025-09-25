🔄 Tutorial: Updating Backends that Use auth_integration
1. Update the auth_integration Package

When you make changes inside the auth_integration repo:

Bump the version in pyproject.toml:

[project]
name = "auth_integration"
version = "0.3.0"   # ⬅️ bump this


Commit and tag the release:

git add .
git commit -m "chore(release): bump version to 0.3.0"
git tag v0.3.0
git push origin main
git push origin v0.3.0


✅ Now GitHub has a new tagged version.

2. Update Backend requirements.txt

Each backend (like Lumen) lists the package.
Open requirements.txt and bump the tag:

auth_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/auth_integration.git@v0.3.0


💡 Using ${GITHUB_TOKEN} ensures private repo access. Keep your token in .env or system keyring.

3. Reinstall the Package

In the backend’s virtual environment:

# Make sure venv is active
pip install --upgrade -r requirements.txt


Check the install log — you should see:

Successfully installed auth_integration-0.3.0

4. Restart the Backend

After updating dependencies, restart your Django server:

# For dev
python manage.py runserver

# For production (example with Daphne)
daphne lumen.asgi:application


If you’re using Docker, rebuild the container:

docker-compose build
docker-compose up -d

5. Verify the Update

Open the backend’s site-packages to confirm the version:

pip show auth_integration


Should print:

Name: auth_integration
Version: 0.3.0


Run a test request (e.g., your /api/templates/carotid/) and check logs.
It should now hit /whoami/ instead of /me/.

6. Recommended Workflows

Dev workflow: You can also create a moving dev tag in your GitHub repo.
Then in requirements.txt:

auth_integration @ git+https://${GITHUB_TOKEN}@github.com/anthonynarine/auth_integration.git@dev


Every time you update the package, re-tag dev:

git tag -f dev
git push origin dev --force


Then just reinstall in your backend.

Release workflow: Use semantic versioning (0.3.0, 0.4.0, etc.) for stable production releases.

🔑 Summary

Update: bump version + tag in auth_integration

Backend: bump requirements.txt to new tag

Reinstall: pip install --upgrade -r requirements.txt

Restart backend and verify with pip show or test requests