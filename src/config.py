"""Config package

Defines Pydantic Settings for use in app and tests.
Environment variables are loaded from .env files, if present.
"""
from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Define app settings"""

    SQLALCHEMY_DATABASE_URL: str

    class Config:
        # load environment variables from .env file
        env_file = ".env"


class TestSettings(BaseSettings):
    """Define test settings"""

    SQLALCHEMY_DATABASE_URL: str

    class Config:
        # load environment variables from .env.test file
        env_file = ".env.test"


@cache
def get_settings() -> Settings:
    """Get app settings

    Settings are cached in memory.

    Returns:
        Settings: app Pydantic Settings
    """
    return Settings()


@cache
def get_test_settings() -> TestSettings:
    """Get test settings

    Settings are cached in memory.

    Returns:
        Settings: test Pydantic Settings
    """
    return TestSettings()
