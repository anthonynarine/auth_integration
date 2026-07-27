# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and adheres to [Semantic Versioning](https://semver.org/).

> Note: entries below `0.3.9` were never backfilled here — see `git log` for the full history if you need it. The `[2.0.0]` entry that used to sit at the top of this file was from a legacy versioning scheme (the package was briefly renamed `gait_integration` and back) and didn't correspond to any real tag; removed for accuracy.

## [0.3.12] - 2026-07-26

### Fixed
- **`ExternalJWTAuthentication` silently returned 403 instead of 401 for auth failures.** DRF rewrites `AuthenticationFailed`/`NotAuthenticated` from 401 to 403 whenever no authenticator advertises a `WWW-Authenticate` header. Added `authenticate_header()` returning `"Bearer"`, so DRF stops downgrading the status. This had been silently disabling every consuming service's token-refresh-on-401 logic — see the root `README.md`'s "Correctness guarantee" section for the full story.

## [0.3.11] - 2026-01-05

### Fixed
- Settings loader when Django is unconfigured; kept `_is_django` alias for backward compatibility.

## [0.3.10] - 2026-01-05

### Changed
- Made package imports framework-agnostic — no FastAPI import path triggered when running under Django.

## [0.3.9] - 2026-01-05

### Added
- DRF auth adapter test coverage (`test_django_authentication.py`).
