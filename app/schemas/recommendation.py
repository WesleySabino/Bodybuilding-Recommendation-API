from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

GoalType = Literal["fat_loss", "muscle_gain", "recomp", "maintenance"]
PhaseType = Literal["cut", "lean_bulk", "recomp", "maintenance"]
CalorieDirection = Literal["deficit", "surplus", "maintenance"]


class RecommendationUserProfile(BaseModel):
    goal: GoalType | None = None
    sex: str | None = None
    training_experience: Literal["beginner", "intermediate", "advanced"] | None = None


class RecommendationMeasurement(BaseModel):
    weight_kg: float | None = Field(default=None, gt=0)
    body_fat_percent: float | None = Field(default=None, ge=1, le=80)
    measured_at: datetime | None = None


class RecommendationRequest(BaseModel):
    profile: RecommendationUserProfile
    latest_measurement: RecommendationMeasurement | None = None
    recent_measurements: list[RecommendationMeasurement] = Field(default_factory=list)


class CalorieGuidance(BaseModel):
    direction: CalorieDirection
    suggested_percent_adjustment: float | None = None
    suggested_daily_calorie_delta: int | None = None


class RecommendationRead(BaseModel):
    phase: PhaseType
    calorie_guidance: CalorieGuidance
    protein_g_per_kg: float
    fat_g_per_kg: float
    carbs_guidance: str
    rationale: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
