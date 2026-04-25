from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bodybuilding Recommendation API"
    environment: str = "development"
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/bodybuilding_api"
    )
    jwt_secret_key: str = Field(
        default="change-me",
        description=(
            "JWT signing secret for development. Override in non-dev environments."
        ),
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    password_hash_algorithm: str = "argon2id"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
