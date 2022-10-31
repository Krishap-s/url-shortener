from typing import Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "url_shortener"
    database_url: str = "sqlite:///:memory:"
    cassandra_host: str = "localhost"
    cassandra_keyspace: str = "url_shortener"
    cassandra_username: Union[None, str]
    cassandra_password: Union[None, str]
    allow_origins: list = ["*"]
    migrate: bool = False
    secret_key: str = "secret"

    class Config:
        env_file = ".env"
        env = {
            "database_url": {"env": "DATABASE_URL"},
            "migrate": {"env": "MIGRATE"},
            "cassandra_host": {"env": "CASSANDRA_HOST"},
            "cassandra_username": {"env": "CASSANDRA_USERNAME"},
            "cassandra_password": {"env": "CASSANDRA_PASSWORD"},
            "cassandra_keyspace": {"env": "CASSANDRA_KEYSPACE"},
        }  # noqa: E501


class TestSettings(BaseSettings):
    app_name: str = "url_shortener"
    database_url: str = "sqlite:///:memory:"
    allow_origins: list = ["*"]
    migrate: bool = True
    secret_key: str = "secret"


settings = Settings()
