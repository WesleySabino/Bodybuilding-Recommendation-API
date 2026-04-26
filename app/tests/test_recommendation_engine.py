from app.schemas.recommendation import (
    RecommendationMeasurement,
    RecommendationRequest,
    RecommendationUserProfile,
)
from app.services.recommendation_engine import generate_recommendation


def test_fat_loss_profile_recommends_cut() -> None:
    request = RecommendationRequest(
        profile=RecommendationUserProfile(goal="fat_loss"),
        latest_measurement=RecommendationMeasurement(
            weight_kg=91.0,
            body_fat_percent=28.0,
        ),
    )

    recommendation = generate_recommendation(request)

    assert recommendation.phase == "cut"
    assert recommendation.calorie_guidance.direction == "deficit"


def test_muscle_gain_with_normal_body_fat_recommends_lean_bulk() -> None:
    request = RecommendationRequest(
        profile=RecommendationUserProfile(goal="muscle_gain"),
        latest_measurement=RecommendationMeasurement(
            weight_kg=76.0,
            body_fat_percent=17.0,
        ),
    )

    recommendation = generate_recommendation(request)

    assert recommendation.phase == "lean_bulk"
    assert recommendation.calorie_guidance.direction == "surplus"


def test_muscle_gain_with_high_body_fat_recommends_recomp_and_warns() -> None:
    request = RecommendationRequest(
        profile=RecommendationUserProfile(goal="muscle_gain"),
        latest_measurement=RecommendationMeasurement(
            weight_kg=90.0,
            body_fat_percent=29.0,
        ),
    )

    recommendation = generate_recommendation(request)

    assert recommendation.phase in {"recomp", "cut"}
    assert any(
        "avoid aggressive bulking" in warning
        for warning in recommendation.warnings
    )


def test_missing_body_fat_still_returns_recommendation_with_warning() -> None:
    request = RecommendationRequest(
        profile=RecommendationUserProfile(goal="muscle_gain"),
        latest_measurement=RecommendationMeasurement(
            weight_kg=84.5,
            body_fat_percent=None,
        ),
    )

    recommendation = generate_recommendation(request)

    assert recommendation.phase == "lean_bulk"
    assert any(
        "Body-fat percentage is missing" in warning
        for warning in recommendation.warnings
    )


def test_maintenance_goal_recommends_maintenance() -> None:
    request = RecommendationRequest(
        profile=RecommendationUserProfile(goal="maintenance"),
        latest_measurement=RecommendationMeasurement(
            weight_kg=80.0,
            body_fat_percent=18.0,
        ),
    )

    recommendation = generate_recommendation(request)

    assert recommendation.phase == "maintenance"
    assert recommendation.calorie_guidance.direction == "maintenance"
