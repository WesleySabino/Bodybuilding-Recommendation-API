# Common API Errors (MVP)

This document summarizes the error semantics used across the MVP API.

## Error response format

Errors return a JSON body with at least:

```json
{
  "detail": "Human-readable message"
}
```

Validation failures (`422`) follow FastAPI/Pydantic's standard list-style error payload.

## Status codes

### 400 Bad Request
Used when request syntax is valid, but required domain state is missing.

Common cases:
- `POST /api/v1/recommendations` with no user profile.
- `POST /api/v1/recommendations` with no measurements.

### 401 Unauthorized
Used for authentication failures.

Common cases:
- Missing bearer token on protected endpoints.
- Invalid/expired token.
- Invalid login credentials (`POST /api/v1/auth/login`).

### 404 Not Found
Used when a requested resource is not found.

Current MVP case:
- `GET /api/v1/measurements/latest` when the authenticated user has no measurements.

### 409 Conflict
Used when attempting to create a resource that conflicts with existing unique state.

Current MVP case:
- `POST /api/v1/auth/register` with an email already in use.

### 422 Unprocessable Entity
Used for schema/validation errors in request body/query params.

Common cases:
- Missing required fields.
- Invalid enum values.
- Numeric constraints violations.
