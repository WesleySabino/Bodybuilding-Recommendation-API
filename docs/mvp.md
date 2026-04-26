# MVP Status — Bodybuilding Recommendation API

This page tracks what is complete for MVP handoff.

## Implemented

- Authentication endpoints:
  - `POST /api/v1/auth/register`
  - `POST /api/v1/auth/login`
- User endpoints:
  - `GET /api/v1/users/me`
  - `PATCH /api/v1/users/me`
- Measurement endpoints:
  - `POST /api/v1/measurements`
  - `GET /api/v1/measurements`
  - `GET /api/v1/measurements/latest`
- Recommendation endpoint:
  - `POST /api/v1/recommendations`
- Deterministic recommendation engine with supported phases:
  - `cut`, `lean_bulk`, `recomp`, `maintenance`
- OpenAPI docs with endpoint summaries/descriptions and explicit common error response codes.
- Tests for health/auth/users/measurements/recommendation behavior.

## Deferred (Post-MVP)

- Recommendation persistence/history endpoint.
- Frontend client(s).
- ML-based personalization.
- Integrations with wearables or external nutrition/training apps.
- Subscription/payments.

## Known limitations

- Recommendations require both profile and at least one measurement; otherwise `400` is returned.
- `GET /api/v1/measurements/latest` returns `404` when no measurements exist.
- Auth uses bearer JWT and a single app-level signing configuration.
- Response payloads are optimized for MVP completeness and may evolve before GA.
