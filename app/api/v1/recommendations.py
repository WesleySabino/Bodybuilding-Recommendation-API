from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User as UserModel
from app.schemas.recommendation import (
    RecommendationMeasurement,
    RecommendationRead,
    RecommendationRequest,
    RecommendationUserProfile,
)
from app.services.measurements import list_recent_measurements
from app.services.recommendation_engine import generate_recommendation
from app.services.users import get_user_profile

RECENT_MEASUREMENTS_LIMIT = 8

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[UserModel, Depends(get_current_user)]


@router.post(
    "",
    response_model=RecommendationRead,
    summary="Generate recommendation for current user",
)
def create_recommendation(
    db: DbSession,
    current_user: CurrentUser,
) -> RecommendationRead:
    profile = get_user_profile(db, current_user.id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User profile is required before requesting recommendations.",
        )

    measurements = list_recent_measurements(
        db,
        current_user.id,
        RECENT_MEASUREMENTS_LIMIT,
    )
    if not measurements:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "At least one measurement is required before requesting "
                "recommendations."
            ),
        )

    latest = measurements[0]
    latest_measurement = RecommendationMeasurement(
        weight_kg=latest.weight_kg,
        body_fat_percent=latest.body_fat_percent,
        measured_at=latest.measured_at,
    )

    recent_measurements = [
        RecommendationMeasurement(
            weight_kg=measurement.weight_kg,
            body_fat_percent=measurement.body_fat_percent,
            measured_at=measurement.measured_at,
        )
        for measurement in reversed(measurements)
    ]

    request = RecommendationRequest(
        profile=RecommendationUserProfile(
            goal=profile.goal,
            sex=profile.sex,
            training_experience=profile.training_experience,
        ),
        latest_measurement=latest_measurement,
        recent_measurements=recent_measurements,
    )

    return generate_recommendation(request)
