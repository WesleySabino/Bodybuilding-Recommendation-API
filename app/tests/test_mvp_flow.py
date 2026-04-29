from datetime import timedelta

from fastapi.testclient import TestClient

from app.core.security import create_access_token

PASSWORD = "strong-password"


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _register_and_login(client: TestClient, email: str) -> str:
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": PASSWORD},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": PASSWORD},
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


def test_full_mvp_happy_path_flow(client: TestClient) -> None:
    token = _register_and_login(client, "mvp-flow@example.com")
    headers = _auth_headers(token)

    me_response = client.get("/api/v1/users/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "mvp-flow@example.com"

    patch_response = client.patch(
        "/api/v1/users/me",
        headers=headers,
        json={
            "sex": "male",
            "height_cm": 182,
            "goal": "fat_loss",
            "training_experience": "intermediate",
        },
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["profile"]["goal"] == "fat_loss"

    create_measurement = client.post(
        "/api/v1/measurements",
        headers=headers,
        json={
            "weight_kg": 88.4,
            "body_fat_percent": 22.2,
            "waist_cm": 94.0,
            "notes": "baseline",
            "measured_at": "2026-01-10T07:30:00+00:00",
        },
    )
    assert create_measurement.status_code == 201

    latest_measurement = client.get("/api/v1/measurements/latest", headers=headers)
    assert latest_measurement.status_code == 200
    assert latest_measurement.json()["weight_kg"] == 88.4

    recommendation_response = client.post("/api/v1/recommendations", headers=headers)
    assert recommendation_response.status_code == 200
    recommendation_body = recommendation_response.json()
    assert recommendation_body["phase"] == "cut"
    assert recommendation_body["calorie_guidance"]["direction"] == "deficit"


def test_multi_user_isolation_for_measurements_and_recommendations(
    client: TestClient,
) -> None:
    token_a = _register_and_login(client, "mvp-isolation-a@example.com")
    token_b = _register_and_login(client, "mvp-isolation-b@example.com")
    headers_a = _auth_headers(token_a)
    headers_b = _auth_headers(token_b)

    client.patch(
        "/api/v1/users/me",
        headers=headers_a,
        json={
            "sex": "male",
            "height_cm": 180,
            "goal": "fat_loss",
            "training_experience": "beginner",
        },
    )
    client.patch(
        "/api/v1/users/me",
        headers=headers_b,
        json={
            "sex": "female",
            "height_cm": 168,
            "goal": "muscle_gain",
            "training_experience": "advanced",
        },
    )

    client.post(
        "/api/v1/measurements",
        headers=headers_a,
        json={
            "weight_kg": 90.0,
            "body_fat_percent": 26.0,
            "measured_at": "2026-01-01T08:00:00+00:00",
        },
    )
    client.post(
        "/api/v1/measurements",
        headers=headers_b,
        json={
            "weight_kg": 70.0,
            "body_fat_percent": 15.0,
            "measured_at": "2026-01-01T08:00:00+00:00",
        },
    )

    list_a = client.get("/api/v1/measurements", headers=headers_a)
    list_b = client.get("/api/v1/measurements", headers=headers_b)

    assert list_a.status_code == 200
    assert list_b.status_code == 200
    assert [m["weight_kg"] for m in list_a.json()["items"]] == [90.0]
    assert [m["weight_kg"] for m in list_b.json()["items"]] == [70.0]

    reco_a = client.post("/api/v1/recommendations", headers=headers_a)
    reco_b = client.post("/api/v1/recommendations", headers=headers_b)

    assert reco_a.status_code == 200
    assert reco_b.status_code == 200
    assert reco_a.json()["calorie_guidance"]["direction"] == "deficit"
    assert reco_b.json()["calorie_guidance"]["direction"] == "surplus"


def test_auth_failures_for_missing_malformed_and_expired_tokens(
    client: TestClient,
) -> None:
    missing_token = client.get("/api/v1/users/me")
    malformed_token = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer definitely.not.a.valid.token"},
    )
    expired_token = create_access_token(
        {"sub": "999"},
        expires_delta=timedelta(seconds=-1),
    )
    expired_response = client.get(
        "/api/v1/users/me",
        headers=_auth_headers(expired_token),
    )

    assert missing_token.status_code == 401
    assert malformed_token.status_code == 401
    assert expired_response.status_code == 401


def test_validation_errors_for_mvp_payloads(client: TestClient) -> None:
    bad_email = client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": PASSWORD},
    )
    missing_password = client.post(
        "/api/v1/auth/register",
        json={"email": "missing-password@example.com"},
    )

    token = _register_and_login(client, "mvp-validation@example.com")
    headers = _auth_headers(token)

    invalid_profile_enum = client.patch(
        "/api/v1/users/me",
        headers=headers,
        json={"goal": "cutting"},
    )
    invalid_measurement = client.post(
        "/api/v1/measurements",
        headers=headers,
        json={"weight_kg": -5, "body_fat_percent": 99, "waist_cm": 0},
    )

    assert bad_email.status_code == 422
    assert missing_password.status_code == 422
    assert invalid_profile_enum.status_code == 422
    assert invalid_measurement.status_code == 422
