from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
