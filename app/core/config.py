from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Capital Group"
    environment: str = "local"
    debug: bool = False
    secret_key: str = Field(default="local-development-secret-change-me", min_length=16)
    admin_email: str = "admin@capitalgroup.fr"
    admin_password: str = "ChangeMe123!"
    database_url: str = "sqlite:///./capital_group.db"
    upload_dir: Path = Path("uploads")
    max_upload_mb: int = 5
    log_level: str = "INFO"
    session_cookie_secure: bool = False
    csrf_cookie_secure: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: object) -> object:
        if isinstance(value, str) and value.lower() in {"release", "prod", "production"}:
            return False
        return value

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
