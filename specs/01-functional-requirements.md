# Functional Requirements

## Authentication

### Register User

A new user can register with:

- `name`
- `password`

Rules:

- `name` must be unique.
- `password` must be hashed before storage.
- API must never return `password_hash`.
- Registration returns the created user profile or an access token, depending on implementation preference.

### Login User

A registered user can log in with:

- `name`
- `password`

Rules:

- Valid credentials return a JWT access token.
- Invalid credentials return `401 Unauthorized`.

## User Profile

A user can view and update their own profile.

Profile fields:

- `id`
- `name`
- `sex`: `male`, `female`, `other`, or `unspecified`
- `height_cm`
- `created_at`
- `updated_at`

Rules:

- `height_cm` must be positive.
- `height_cm` should be realistic, for example `80 <= height_cm <= 250`.
- Only authenticated users can access their own profile.

## Daily Weight Tracking

Users can create and list bodyweight entries.

Fields:

- `id`
- `user_id`
- `weight_kg`
- `entry_date`
- `created_at`

Rules:

- `weight_kg` must be positive.
- Recommended validation range: `20 <= weight_kg <= 400`.
- `entry_date` defaults to current date if omitted.
- One weight entry per user per date.
- Authenticated users can only access their own entries.

## Weekly Waist Tracking

Users can create and list waist circumference entries.

Fields:

- `id`
- `user_id`
- `waist_cm`
- `entry_date`
- `created_at`

Rules:

- `waist_cm` must be positive.
- Recommended validation range: `40 <= waist_cm <= 250`.
- `entry_date` defaults to current date if omitted.
- One waist entry per user per date.
- The API does not need to enforce exactly weekly spacing in MVP, but should document that waist is intended to be entered weekly.

## Recommendation

Authenticated users can request their current recommendation.

The endpoint calculates:

- latest weight
- latest waist
- BMI
- waist-to-height ratio
- weekly weight change percentage
- waist change in centimeters
- phase recommendation
- explanation
- confidence level

Recommendations:

- `bulk`
- `lean_bulk`
- `cut`
- `maintain_or_recomposition`

Confidence:

- `low`
- `medium`
- `high`

## Recommendation History

The MVP may store recommendation snapshots when `GET /recommendations/current` is called.

Fields:

- `id`
- `user_id`
- `bmi`
- `waist_to_height_ratio`
- `weekly_weight_change_pct`
- `waist_change_cm`
- `recommendation`
- `confidence`
- `explanation`
- `created_at`

## Error Handling

Use consistent JSON errors:

```json
{
  "detail": "Human-readable error message"
}
```

Expected errors:

- `400 Bad Request` for invalid input or duplicate same-day measurement.
- `401 Unauthorized` for missing or invalid token.
- `403 Forbidden` if cross-user access is attempted.
- `404 Not Found` for missing resource.
- `409 Conflict` for duplicate name or duplicate measurement date.
