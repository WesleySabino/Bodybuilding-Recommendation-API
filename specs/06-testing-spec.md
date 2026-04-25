# Testing Specification

## Test Framework

Use:

- pytest
- FastAPI TestClient or httpx AsyncClient
- temporary test database
- factory fixtures for users and measurements

## Required Test Categories

## Health

- `GET /health` returns `200` and `status: ok`.

## Auth Tests

### Registration

- Can register with valid name and password.
- Cannot register duplicate name.
- Password hash is stored, raw password is not stored.
- Response does not include `password_hash`.

### Login

- Can login with valid credentials.
- Cannot login with wrong password.
- Cannot login with unknown name.
- Login returns bearer token.

## User Tests

- Authenticated user can get own profile.
- Unauthenticated request fails.
- Authenticated user can update sex and height.
- Invalid height is rejected.
- Invalid sex enum is rejected.

## Weight Measurement Tests

- Authenticated user can create weight entry.
- `entry_date` defaults to today if omitted.
- Duplicate weight entry for same date is rejected.
- Invalid weight is rejected.
- User cannot see another user's weight entries.
- List endpoint returns entries ordered by date descending.

## Waist Measurement Tests

- Authenticated user can create waist entry.
- `entry_date` defaults to today if omitted.
- Duplicate waist entry for same date is rejected.
- Invalid waist is rejected.
- User cannot see another user's waist entries.
- List endpoint returns entries ordered by date descending.

## Recommendation Formula Unit Tests

Test pure functions separately from API endpoints.

### BMI

```text
height_cm = 180
weight_kg = 81
expected_bmi = 25.0
```

### Waist-to-Height Ratio

```text
waist_cm = 90
height_cm = 180
expected_whtr = 0.5
```

### Weekly Weight Change

```text
previous_avg = 80
current_avg = 80.8
expected_pct = 1.0
```

### Waist Change

```text
previous_waist = 84
latest_waist = 85.5
expected_change = 1.5
```

## Recommendation Branch Tests

- BMI below 18.5 returns `bulk`.
- WHtR greater than or equal to 0.50 returns `cut`.
- BMI greater than or equal to 27 returns `cut`.
- BMI 18.5–24.9 and WHtR below 0.50 returns `lean_bulk`.
- Otherwise returns `maintain_or_recomposition`.
- Missing height returns `400` from API.
- Missing weight returns `400` from API.
- Missing waist uses BMI-only fallback with low confidence.

## Confidence Tests

- Fewer than 7 weight entries returns `low`.
- At least 7 weight entries and fewer than 2 waist entries returns `medium`.
- At least 14 weight entries and at least 2 waist entries returns `high`.

## Snapshot Tests

- Calling current recommendation creates a recommendation snapshot if this feature is implemented.
- Snapshot belongs to authenticated user.
- History endpoint returns only authenticated user's snapshots.

## Minimum Acceptance Criteria

Before considering MVP complete:

```text
pytest passes
ruff or equivalent linter passes
migrations apply cleanly
docker compose up starts the API
OpenAPI docs load at /docs
README curl examples work
```
