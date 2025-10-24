# Testing Guide for gait_integration

## Overview
This guide describes the testing strategy used for the `gait_integration` package.
The suite ensures correct behavior for authentication validation, exception handling,
permissions, utility helpers, and environment configuration.

---

## Test Environment Setup

The `tests/conftest.py` file initializes environment variables and mock settings so that
tests can run independently of Django. It defines safe defaults for `GAIT_AUTH_URL` and
`GAIT_TIMEOUT` and avoids `ImproperlyConfigured` errors.

All tests are executed using **pytest** with **pytest‑asyncio** enabled.

---

## Test Modules

| File | Purpose |
|------|----------|
| `test_client.py` | Validates async token validation logic for `/api/whoami/`. |
| `test_exceptions.py` | Ensures DRF exception classes use correct codes and messages. |
| `test_permissions.py` | Confirms role‑based permission checks behave as expected. |
| `test_utils.py` | Tests claim helper functions and role evaluation utilities. |
| `test_settings.py` | Validates environment variable loading and Django fallback logic. |

---

## Running Tests

```bash
pytest -v -s
```

Pytest configuration is included in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

## Coverage Goals

- 100% function coverage across all core modules.
- No external API calls — all network operations are mocked.
- Reusable test patterns for any service integrating with Gait.

---

Maintained by **Anthony Narine**, 2025
