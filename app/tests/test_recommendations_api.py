from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient


def _register_and_login(client: TestClient, email: str) -> str:
    password = "strong-password"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    return response.json()["access_token"]


def _create_profile(client: TestClient, token: str, goal: str = "fat_loss") -> None:
    client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sex": "male",
            "height_cm": 180,
            "goal": goal,
            "training_experience": "intermediate",
        },
    )


def _create_measurement(
    client: TestClient,
    token: str,
    weight_kg: float,
    measured_at: datetime,
    body_fat_percent: float | None = None,
) -> None:
    client.post(
        "/api/v1/measurements",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "weight_kg": weight_kg,
            "body_fat_percent": body_fat_percent,
            "measured_at": measured_at.isoformat(),
        },
    )


def test_recommendations_requires_authentication(client: TestClient) -> None:
    response = client.post("/api/v1/recommendations")

    assert response.status_code == 401


def test_recommendations_returns_payload_for_user_with_profile_and_measurement(
    client: TestClient,
) -> None:
    token = _register_and_login(client, "reco-happy@example.com")
    _create_profile(client, token, goal="fat_loss")
    now = datetime.now(timezone.utc)  # noqa: UP017
    _create_measurement(
        client,
        token,
        weight_kg=92.0,
        body_fat_percent=26.0,
        measured_at=now - timedelta(days=7),
    )
    _create_measurement(
        client,
        token,
        weight_kg=91.0,
        body_fat_percent=25.0,
        measured_at=now,
    )

    response = client.post(
        "/api/v1/recommendations",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["phase"] == "cut"
    assert body["calorie_guidance"]["direction"] == "deficit"
    assert any("Recent weight trend is" in line for line in body["rationale"])


def test_recommendations_returns_400_when_profile_is_missing(
    client: TestClient,
) -> None:
    token = _register_and_login(client, "reco-no-profile@example.com")
    now = datetime.now(timezone.utc)  # noqa: UP017
    _create_measurement(client, token, weight_kg=81.0, measured_at=now)

    response = client.post(
        "/api/v1/recommendations",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "User profile is required before requesting recommendations.",
    }


def test_recommendations_returns_400_when_measurement_is_missing(
    client: TestClient,
) -> None:
    token = _register_and_login(client, "reco-no-measurement@example.com")
    _create_profile(client, token, goal="maintenance")

    response = client.post(
        "/api/v1/recommendations",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "At least one measurement is required before requesting "
            "recommendations."
        ),
    }


def test_recommendations_are_scoped_to_current_user_data(client: TestClient) -> None:
    token_a = _register_and_login(client, "reco-scope-a@example.com")
    token_b = _register_and_login(client, "reco-scope-b@example.com")
    now = datetime.now(timezone.utc)  # noqa: UP017

    _create_profile(client, token_a, goal="fat_loss")
    _create_measurement(
        client,
        token_a,
        weight_kg=89.0,
        body_fat_percent=28.0,
        measured_at=now,
    )

    _create_profile(client, token_b, goal="muscle_gain")
    _create_measurement(
        client,
        token_b,
        weight_kg=75.0,
        body_fat_percent=15.0,
        measured_at=now,
    )

    response = client.post(
        "/api/v1/recommendations",
        headers={"Authorization": f"Bearer {token_a}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["phase"] == "cut"
    assert body["calorie_guidance"]["direction"] == "deficit"
