# docs/ index

The root [`README.md`](../README.md) is the canonical entry point — installation, quickstart (Django + FastAPI), the ecosystem diagram, the 401-vs-403 correctness guarantee, and the release process all live there. This directory holds deeper/narrower references:

| Doc | Covers |
|---|---|
| [`CHANGELOG.md`](./CHANGELOG.md) | Version history. |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | PR workflow and coding standards. |
| [`SECURITY_POLICY.md`](./SECURITY_POLICY.md) | Supported versions, vulnerability reporting. |
| [`TESTING_GUIDE.md`](./TESTING_GUIDE.md) | Test suite layout and how to run it. |
| [`VERSION_BUMP_GUIDE.md`](./VERSION_BUMP_GUIDE.md) | Using `bump_version.sh`, and the GitHub Release step it doesn't do for you. |
| [`RELEASE_CHECKLIST.MD`](./RELEASE_CHECKLIST.MD) | The full step-by-step release checklist. |
| [`UPDATE_BACKENDS.md`](./UPDATE_BACKENDS.md) | Updating a consuming service (`lumen_reports`, `lumen_ai/brain/backend`) after a new release. |

Module-level docs (what each file inside the package actually does) live next to the code: `auth_integration/docs/` and `auth_integration/django/docs/`.

For the full request-lifecycle trace across React, this package, and Gait — including real bugs found and fixed — see Lumen's own docs: `Lumen/docs/security/Auth_Token_Lifecycle_End_To_End.md`.

---

Maintained by **Anthony Narine**
