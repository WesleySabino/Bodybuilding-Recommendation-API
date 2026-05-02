from functools import lru_cache
import logging

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



def _warn_if_insecure_production_settings(settings: "Settings") -> None:
    is_production = settings.environment.lower() == "production"
    weak_secret_values = {"", "change-me", "dev-only-change-me", "secret", "password"}

    if is_production and settings.jwt_secret_key.lower() in weak_secret_values:
        logging.getLogger(__name__).warning(
            "JWT_SECRET_KEY appears insecure for production. Set a long random value."
        )

@lru_cache
def get_settings() -> Settings:
    loaded_settings = Settings()
    _warn_if_insecure_production_settings(loaded_settings)
    return loaded_settings


settings = get_settings()
