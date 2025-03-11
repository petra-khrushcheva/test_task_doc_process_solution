import pathlib

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    database_url: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20


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
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_config(self) -> DatabaseConfig:
        """Возвращает объект конфигурации базы данных."""
        return DatabaseConfig(
            database_url=self.database_url,
        )
