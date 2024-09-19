import logging
import os
from typing import ClassVar

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Base configuration class.
    Subclasses should include configurations for testing, development and production environments.
    """

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    SERVICE_NAME: str = "trello-example"

    API_PREFIX: str = f"/api"

    DOCS_URL: str = f"/swagger"

    LOGGER_FILENAME: str = f"/var/tmp/app.{SERVICE_NAME}.log"
    LOGGER_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message} {extra}"

    CORS_ORIGINS: str = "*"

    POSTGRES_USERNAME: str = Field("admin", env="POSTGRES_USERNAME")
    POSTGRES_PASSWORD: str = Field("admin", env="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field("postgresql", env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field("5432", env="POSTGRES_PORT")
    POSTGRES_DBNAME: str = Field("admin_default", env="POSTGRES_DBNAME")
    DATABASE_URL: str = ""

    DB_POOL_SIZE_MIN: int = 5
    DB_POOL_SIZE_MAX: int = 80

    SQLALCHEMY_ECHO: bool = False

    REDIS_URL: str = "redis://localhost:6379/0"

    DOCUMENT_ROOT: ClassVar[str] = '/opt'

    ENVIRONMENT: str = Field("local", env="ENVIRONMENT")

    TOKEN_GENERATION_ALGORITHM: str = "HS256"
    SECRET_KEY: str = Field("", env="SECRET_KEY")

    REFRESH_SECRET_KEY: str = "your_refresh_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    SESSION_SECRET_KEY: str = Field("", env="SESSION_SECRET_KEY")


    @field_validator("DATABASE_URL", mode="before")
    def validate_database_url(cls, value: str, values: ValidationInfo) -> str:
        if value:
            return value
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
            user=values.data.get("POSTGRES_USERNAME"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            port=values.data.get("POSTGRES_PORT"),
            name=values.data.get("POSTGRES_DBNAME"),
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
logging.basicConfig()
