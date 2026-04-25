from fastapi.testclient import TestClient


def _register_and_login(client: TestClient, email: str = "me@example.com") -> str:
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


def test_users_me_requires_authentication(client: TestClient) -> None:
    get_response = client.get("/api/v1/users/me")
    patch_response = client.patch("/api/v1/users/me", json={"goal": "fat_loss"})

    assert get_response.status_code == 401
    assert patch_response.status_code == 401


def test_get_users_me_returns_registered_user(client: TestClient) -> None:
    token = _register_and_login(client)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] > 0
    assert body["email"] == "me@example.com"
    assert body["profile"] is None


def test_patch_users_me_creates_profile(client: TestClient) -> None:
    token = _register_and_login(client)

    response = client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sex": "male",
            "height_cm": 180,
            "goal": "fat_loss",
            "training_experience": "beginner",
        },
    )

    assert response.status_code == 200
    profile = response.json()["profile"]
    assert profile is not None
    assert profile["sex"] == "male"
    assert profile["height_cm"] == 180
    assert profile["goal"] == "fat_loss"
    assert profile["training_experience"] == "beginner"


def test_patch_users_me_only_updates_provided_fields(client: TestClient) -> None:
    token = _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    client.patch(
        "/api/v1/users/me",
        headers=headers,
        json={
            "sex": "female",
            "height_cm": 165,
            "goal": "muscle_gain",
            "training_experience": "intermediate",
        },
    )

    response = client.patch(
        "/api/v1/users/me",
        headers=headers,
        json={"goal": "maintenance"},
    )

    assert response.status_code == 200
    profile = response.json()["profile"]
    assert profile == {
        "sex": "female",
        "birth_date": None,
        "height_cm": 165.0,
        "training_experience": "intermediate",
        "goal": "maintenance",
    }


def test_patch_users_me_rejects_invalid_enum_and_height(client: TestClient) -> None:
    token = _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    invalid_goal = client.patch(
        "/api/v1/users/me",
        headers=headers,
        json={"goal": "cutting"},
    )
    invalid_height = client.patch(
        "/api/v1/users/me",
        headers=headers,
        json={"height_cm": 0},
    )

    assert invalid_goal.status_code == 422
    assert invalid_height.status_code == 422
