from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MeasurementCreate(BaseModel):
    weight_kg: float = Field(gt=0)
    body_fat_percent: float | None = Field(default=None, ge=1, le=80)
    waist_cm: float | None = Field(default=None, gt=0)
    notes: str | None = None
    measured_at: datetime | None = None


class MeasurementRead(BaseModel):
    id: int
    user_id: int
    weight_kg: float
    body_fat_percent: float | None = None
    waist_cm: float | None = None
    notes: str | None = None
    measured_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MeasurementListRead(BaseModel):
    items: list[MeasurementRead]
    total: int
    limit: int
    offset: int
