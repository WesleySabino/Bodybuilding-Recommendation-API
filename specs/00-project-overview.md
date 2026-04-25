# Bodybuilding Recommendation API — MVP Project Overview

## Purpose

Build a backend-only REST API that allows a user to register, maintain a basic body profile, record body measurements, and receive a bodybuilding phase recommendation: `bulk`, `lean_bulk`, `cut`, or `maintain_or_recomposition`.

The MVP is not a medical diagnosis tool. It provides simple fitness-oriented guidance based on BMI, waist-to-height ratio, weight trend, and waist trend.

## Target User

A bodybuilding or fitness trainee who wants a simple way to track bodyweight and waist circumference and receive a high-level recommendation about whether to bulk, cut, or maintain.

## MVP Scope

Included:

- User registration with name and password.
- Login with JWT authentication.
- User profile with sex and height.
- Daily weight entries.
- Weekly waist circumference entries.
- Current recommendation endpoint.
- Basic recommendation history snapshots.
- Dockerized local development environment.
- Automated tests.

Excluded from MVP:

- Frontend.
- Calorie or macro calculation.
- Training plan generation.
- Medical risk scoring.
- Password recovery.
- Email verification.
- Social login.
- Admin panel.
- Multi-tenant organizations.

## Recommended Tech Stack

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- JWT authentication
- Argon2 or bcrypt password hashing
- Docker Compose
- pytest

## Implementation Priorities

1. Project scaffold and health endpoint.
2. Database setup and migrations.
3. Auth and user profile.
4. Measurement tracking.
5. Recommendation engine.
6. Tests and README examples.

## External Guidance Notes

FastAPI supports relational database integrations and does not force a specific ORM, which makes SQLAlchemy/PostgreSQL appropriate for this MVP. Alembic is the standard migration tool for SQLAlchemy-based projects. Passwords must be stored with purpose-built password hashing, not reversible encryption; OWASP recommends modern password hashing approaches such as Argon2id, bcrypt, scrypt, or PBKDF2 depending on the platform.
