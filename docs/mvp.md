# Bodybuilding Recommendation API — MVP Contract

## Purpose

This document defines the **Minimum Viable Product (MVP)** contract for the backend-only bodybuilding recommendation API.

The MVP focuses on:
- basic account access,
- profile and progress data capture,
- deterministic nutrition-phase recommendations.

It intentionally avoids advanced integrations and optimization features to keep initial delivery small, testable, and stable.

## Scope

### In scope
- Authentication (register/login).
- Authenticated current-user retrieval/update.
- Body measurement logging and retrieval.
- On-demand recommendation generation from profile + latest measurements.

### Out of scope for MVP
- Mobile/web frontend clients.
- ML-based personalization.
- External device or app integrations.

## Domain Model (Minimal)

### 1) User account
Represents an authenticated person using the API.

Minimum fields:
- `id` (UUID)
- `email` (unique)
- `password_hash`
- `created_at`
- `updated_at`

### 2) User profile
Represents user context needed to produce useful recommendations.

Minimum fields:
- `user_id` (FK to user)
- `sex` (`male`, `female`, `other`)
- `birth_date` **or** derived `age`
- `height_cm`
- `training_experience` (`beginner`, `intermediate`, `advanced`)
- `goal` (`fat_loss`, `muscle_gain`, `recomposition`, `maintenance`)
- `updated_at`

### 3) Body measurement entry
Time-series progress snapshot.

Minimum fields:
- `id` (UUID)
- `user_id` (FK)
- `weight_kg`
- `body_fat_pct` (nullable)
- `waist_cm` (nullable)
- `notes` (nullable)
- `measured_at` (datetime)
- `created_at`

### 4) Recommendation result
A generated recommendation payload saved/audited per request.

Minimum fields:
- `id` (UUID)
- `user_id` (FK)
- `phase` (`cut`, `lean_bulk`, `recomp`, `maintenance`)
- `calories_guidance` (text/object)
- `protein_guidance` (text/object)
- `fat_guidance` (text/object)
- `carbs_guidance` (text/object)
- `rationale` (array/text explanation)
- `warnings` (array of strings)
- `generated_at`

## MVP Phases

MVP recommendation engine must output exactly one of:
- `cut`
- `lean_bulk`
- `recomp`
- `maintenance`

### High-level intent
- **cut**: reduce body fat while preserving muscle.
- **lean_bulk**: gain muscle with controlled fat gain.
- **recomp**: slowly improve composition near maintenance.
- **maintenance**: maintain weight/composition with consistency.

## MVP API Endpoints

All routes are mounted under `/api/v1`.

### Auth
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`

### Users
- `GET /api/v1/users/me`
- `PATCH /api/v1/users/me`

### Measurements
- `POST /api/v1/measurements`
- `GET /api/v1/measurements`
- `GET /api/v1/measurements/latest`

### Recommendations
- `POST /api/v1/recommendations`

## Functional Rules (MVP-level)

1. All non-auth endpoints require Bearer token auth.
2. `users/me` returns only the authenticated user context.
3. Measurements are per-user and ordered by `measured_at` descending for list/default views.
4. `measurements/latest` returns the most recent measurement or 404 if none exists.
5. Recommendation generation uses:
   - profile completeness,
   - latest measurement,
   - deterministic phase/macronutrient guidance logic.
6. Recommendation response always includes `phase`, macro guidance, `rationale`, and any `warnings`.

## Non-Goals (Explicit)

The following are **not** part of MVP:
- No machine learning yet.
- No wearable integration.
- No meal planning.
- No payment/subscription.
- No frontend.

## Acceptance Criteria for MVP Planning

Planning is complete when:
1. Domain model and endpoint contract are documented.
2. Input/output examples exist for each endpoint.
3. Non-goals are explicit and agreed.
4. Runtime implementation can proceed without further product-level ambiguity.
