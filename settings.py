import sys

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "url_shortener"
    database_url: str = "sqlite:///:memory:"
    allow_origins: list = ["*"]
    migrate: bool = False

    class Config:
        env_file = ".env"


class TestSettings(BaseSettings):
    app_name: str = "url_shortener"
    database_url: str = "sqlite:///:memory:"
    allow_origins: list = ["*"]
    migrate: bool = True


# Give different settings when run from pytest
if "pytest" in sys.argv[0]:
    settings = TestSettings()
else:
    settings = Settings()
