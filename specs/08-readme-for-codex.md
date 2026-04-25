# Instructions for Codex

You are implementing a backend-only MVP API from these specs.

## Read Order

1. `00-project-overview.md`
2. `01-functional-requirements.md`
3. `02-domain-formulas.md`
4. `03-api-contract.md`
5. `04-data-model.md`
6. `05-architecture.md`
7. `06-testing-spec.md`
8. `07-codex-implementation-plan.md`

## Hard Rules

- Do not build a frontend.
- Do not add features outside the MVP unless necessary for the listed requirements.
- Keep business formulas in the service layer or pure utility functions.
- Keep routers thin.
- Every authenticated query must be scoped by `user_id`.
- Never return `password_hash`.
- Store passwords only as secure hashes.
- Use metric units only.
- Add tests with each feature.

## Preferred Implementation Style

- Small commits or implementation chunks.
- One feature at a time.
- Tests first or tests immediately after implementation.
- Clear errors.
- Simple code over premature abstraction.

## Definition of Done

The MVP is done when:

- User can register and login.
- User can update sex and height.
- User can add daily weight.
- User can add weekly waist circumference.
- User can request current recommendation.
- Tests pass.
- Docker Compose runs the API and database.
- README explains setup and example requests.
