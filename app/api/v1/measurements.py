from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.measurement import Measurement
from app.models.user import User
from app.schemas.measurement import MeasurementCreate, MeasurementRead

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "",
    response_model=MeasurementRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a measurement for the current user",
)
def create_measurement(
    payload: MeasurementCreate,
    db: DbSession,
    current_user: CurrentUser,
) -> MeasurementRead:
    measurement = Measurement(
        user_id=current_user.id,
        weight_kg=payload.weight_kg,
        body_fat_percent=payload.body_fat_percent,
        waist_cm=payload.waist_cm,
        notes=payload.notes,
        measured_at=payload.measured_at or datetime.now(timezone.utc),  # noqa: UP017
    )
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


@router.get(
    "",
    response_model=list[MeasurementRead],
    summary="List current user's measurements",
)
def list_measurements(
    db: DbSession,
    current_user: CurrentUser,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0, le=10_000),
) -> list[MeasurementRead]:
    statement = (
        select(Measurement)
        .where(Measurement.user_id == current_user.id)
        .order_by(desc(Measurement.measured_at), desc(Measurement.id))
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement))


@router.get(
    "/latest",
    response_model=MeasurementRead,
    summary="Get the latest measurement for the current user",
)
def get_latest_measurement(
    db: DbSession,
    current_user: CurrentUser,
) -> MeasurementRead:
    statement = (
        select(Measurement)
        .where(Measurement.user_id == current_user.id)
        .order_by(desc(Measurement.measured_at), desc(Measurement.id))
        .limit(1)
    )
    measurement = db.scalar(statement)
    if measurement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No measurements found",
        )

    return measurement
