import logging
import pathlib
from typing import Dict

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    """Конфигурация подключения к базе данных для asyncpg."""

    user: str
    password: str
    database: str
    host: str
    port: int
    min_size: int = 1
    max_size: int = 10
    timeout: int = 10

    def as_dict(self) -> Dict[str, str]:
        """
        Возвращает конфигурацию в формате,
        который принимает asyncpg.create_pool().
        """
        return self.model_dump()


class LogConfig(BaseModel):
    level: str = logging.INFO


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{pathlib.Path(__file__).parents[1]}/.env",
        extra="ignore",
    )

    # PostgreSQL database settings
    postgres_host: str
    postgres_port: str
    postgres_db: str
    postgres_password: str
    postgres_user: str

    @property
    def asyncpg_database_config(self) -> dict:
        """
        Создаёт объект конфигурации базы данных в виде словаря для asyncpg.
        """
        return DatabaseConfig(
            user=self.postgres_user,
            password=self.postgres_password,
            database=self.postgres_db,
            host=self.postgres_host,
            port=self.postgres_port,
        ).as_dict()

    @property
    def log_config(self) -> LogConfig:
        return LogConfig()
