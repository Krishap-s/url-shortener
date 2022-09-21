from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "url_shortener"
    database_url: str = "sqlite:///:memory:"
    allow_origins: list = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()