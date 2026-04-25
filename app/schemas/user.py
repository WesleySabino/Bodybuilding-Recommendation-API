from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserProfileRead(BaseModel):
    sex: str | None = None
    birth_date: date | None = None
    height_cm: float | None = None
    training_experience: Literal["beginner", "intermediate", "advanced"] | None = None
    goal: Literal["fat_loss", "muscle_gain", "recomp", "maintenance"] | None = None

    model_config = ConfigDict(from_attributes=True)


class UserProfileUpdate(BaseModel):
    sex: str | None = None
    birth_date: date | None = None
    height_cm: float | None = Field(default=None, gt=0)
    training_experience: Literal["beginner", "intermediate", "advanced"] | None = None
    goal: Literal["fat_loss", "muscle_gain", "recomp", "maintenance"] | None = None


class UserMeRead(BaseModel):
    id: int
    email: EmailStr
    profile: UserProfileRead | None = None

    model_config = ConfigDict(from_attributes=True)
