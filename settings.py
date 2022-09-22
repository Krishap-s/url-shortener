import sys

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "url_shortener"
    database_url: str = "sqlite:///:memory:"
    allow_origins: list = ["*"]
    migrate: bool = False

    class Config:
        env_file = ".env"
        env = {
            "database_url": {"env": "DATABASE_URL"},
            "migrate": {"env": "MIGRATE"},
        }  # noqa: E501


class TestSettings(BaseSettings):
    app_name: str = "url_shortener"
    database_url: str = "sqlite:///:memory:"
    allow_origins: list = ["*"]
    migrate: bool = True

    class Config:
        env_file = "test.env"
        env = {
            "database_url": {"env": "DATABASE_URL"},
        }


# Give different settings when run from pytest
if "pytest" in sys.argv[0]:
    settings = TestSettings()
else:
    settings = Settings()
