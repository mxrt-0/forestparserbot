from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar, final


@final
class Settings(BaseSettings):
    main_env: ClassVar = ".dev.env"
    fallback_env: ClassVar = ".prod.env"
    model_config = SettingsConfigDict(
        env_file=(fallback_env, main_env), env_file_encoding="utf-8"
    )

    BOT_TOKEN: str
    BOT_SECRET_TOKEN: str
    CRYPTOBOT_TOKEN: str
    CRYPTOTESTNETBOT_TOKEN: str
    BASE_URL: str
    WEBHOOK_BOT_PATH: str
    DB_URL: str
    REDIS_URL: str
    BOT_PHOTO: str
    ADMINS: list[int]
    SUPPORT: str
    REQUIRED_CHANNELS: dict[str, dict[str, str | int]]


@lru_cache
def get_settings() -> Settings:
    return Settings()
