from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.measurement import MeasurementCreate, MeasurementRead
from app.services.measurements import (
    create_measurement as create_measurement_record,
)
from app.services.measurements import (
    get_latest_measurement as get_latest_measurement_record,
)
from app.services.measurements import (
    list_measurements as list_measurement_records,
)

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "",
    response_model=MeasurementRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a measurement for the current user",
    description=(
        "Creates a new body measurement entry for the authenticated user at the "
        "provided timestamp (or current time when omitted)."
    ),
    responses={
        401: {"description": "Authentication failure or missing bearer token."},
        422: {"description": "Validation error in request payload."},
    },
)
def create_measurement(
    payload: MeasurementCreate,
    db: DbSession,
    current_user: CurrentUser,
) -> MeasurementRead:
    return create_measurement_record(db, current_user.id, payload)


@router.get(
    "",
    response_model=list[MeasurementRead],
    summary="List current user's measurements",
    description=(
        "Returns a paginated slice of measurements for the authenticated user, "
        "sorted by measured_at descending."
    ),
    responses={
        401: {"description": "Authentication failure or missing bearer token."},
        422: {"description": "Validation error in query parameters."},
    },
)
def list_measurements(
    db: DbSession,
    current_user: CurrentUser,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0, le=10_000),
) -> list[MeasurementRead]:
    return list_measurement_records(db, current_user.id, limit, offset)


@router.get(
    "/latest",
    response_model=MeasurementRead,
    summary="Get the latest measurement for the current user",
    description=(
        "Returns the newest measurement entry for the authenticated user. "
        "Responds with 404 when no measurements exist."
    ),
    responses={
        401: {"description": "Authentication failure or missing bearer token."},
        404: {"description": "No measurements found for the current user."},
    },
)
def get_latest_measurement(
    db: DbSession,
    current_user: CurrentUser,
) -> MeasurementRead:
    measurement = get_latest_measurement_record(db, current_user.id)
    if measurement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No measurements found",
        )

    return measurement
