from datetime import datetime, timezone

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementCreate


def create_measurement(
    db: Session,
    user_id: int,
    payload: MeasurementCreate,
) -> Measurement:
    measurement = Measurement(
        user_id=user_id,
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


def list_measurements(
    db: Session,
    user_id: int,
    limit: int,
    offset: int,
) -> tuple[list[Measurement], int]:
    statement = (
        select(Measurement)
        .where(Measurement.user_id == user_id)
        .order_by(desc(Measurement.measured_at), desc(Measurement.id))
        .limit(limit)
        .offset(offset)
    )
    total_statement = select(func.count()).select_from(Measurement).where(
        Measurement.user_id == user_id
    )
    return list(db.scalars(statement)), db.scalar(total_statement) or 0


def get_latest_measurement(db: Session, user_id: int) -> Measurement | None:
    statement = (
        select(Measurement)
        .where(Measurement.user_id == user_id)
        .order_by(desc(Measurement.measured_at), desc(Measurement.id))
        .limit(1)
    )
    return db.scalar(statement)


def list_recent_measurements(
    db: Session,
    user_id: int,
    limit: int,
) -> list[Measurement]:
    statement = (
        select(Measurement)
        .where(Measurement.user_id == user_id)
        .order_by(desc(Measurement.measured_at), desc(Measurement.id))
        .limit(limit)
    )
    return list(db.scalars(statement))
