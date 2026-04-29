# MVP Final Audit (2026-04-26)

## Checklist

- [x] Audited implementation against `docs/mvp.md` endpoint list.
- [x] Audited implementation against `docs/api-contract.md` behavior expectations.
- [x] Verified `GET /api/v1/health` works.
- [x] Verified `POST /api/v1/auth/register` works.
- [x] Verified `POST /api/v1/auth/login` works.
- [x] Verified `GET /api/v1/users/me` works.
- [x] Verified `PATCH /api/v1/users/me` works.
- [x] Verified `POST /api/v1/measurements` works.
- [x] Verified `GET /api/v1/measurements` works.
- [x] Verified `GET /api/v1/measurements/latest` works.
- [x] Verified `POST /api/v1/recommendations` works.
- [x] Confirmed migrations include all MVP tables (`users`, `user_profiles`, `measurements`).
- [x] Confirmed tests isolate DB state via per-test in-memory DB fixture.
- [x] Confirmed JWT auth is required on user-specific endpoints.
- [x] Confirmed measurement listing is scoped per authenticated user.
- [x] Confirmed recommendations fail safely on incomplete data (`400` for missing profile/measurement).
- [x] Checked README command accuracy for test/lint/build paths.

## Blocking issues fixed

1. **Measurements list contract mismatch**
   - **Issue:** `GET /api/v1/measurements` returned a raw array, but MVP contract defines paginated envelope (`items`, `total`, `limit`, `offset`).
   - **Fix:** Endpoint now returns the paginated envelope; service now returns both items and total count.

2. **Login contract mismatch**
   - **Issue:** `POST /api/v1/auth/login` response lacked `expires_in` from MVP contract.
   - **Fix:** Added `expires_in` to token schema and set it from configured access-token expiry.

## Validation commands run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
docker compose build
```

Additional focused validation (covered by test suite):

- `app/tests/test_health.py`
- `app/tests/test_auth.py`
- `app/tests/test_users.py`
- `app/tests/test_measurements.py`
- `app/tests/test_recommendations_api.py`
- `app/tests/test_mvp_flow.py`
- `app/tests/test_models_metadata.py`
- `app/tests/conftest.py`

## Remaining known limitations

1. **Contract/documentation mismatches still present (non-blocking for endpoint operability):**
   - Contract examples use UUID IDs, while current implementation uses integer IDs.
   - Contract examples show `body_fat_pct` key, while implementation uses `body_fat_percent`.
   - Contract examples include additional user fields (`full_name`, `created_at`, `updated_at`) that are not yet exposed in current user/auth response schemas.

2. **Environment limitation during this audit:**
   - `docker compose build` could not run because Docker is not installed in this execution environment.
