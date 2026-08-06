"""Platform configuration settings models using pydantic-settings."""

from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    """Application metadata settings."""

    name: str = "NeuroFlow AI"
    version: str = "0.1.0"
    environment: Literal["development", "testing", "staging", "production"] = (
        "development"
    )
    debug: bool = False


class RuntimeSettings(BaseModel):
    """Execution runtime engine settings."""

    worker_concurrency: int = Field(default=10, ge=1)
    task_timeout_seconds: int = Field(default=300, ge=1)
    max_retry_attempts: int = Field(default=3, ge=0)


class DatabaseSettings(BaseModel):
    """PostgreSQL and relational database persistence settings."""

    host: str = "localhost"
    port: int = Field(default=5432, ge=1, le=65535)
    database: str = "neuroflow"
    user: str = "postgres"
    password: str = "postgres"
    pool_size: int = Field(default=20, ge=1)
    max_overflow: int = Field(default=10, ge=0)

    @property
    def connection_url(self) -> str:
        """Return SQLAlchemy database connection URI string."""
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )


class LoggingSettings(BaseModel):
    """Platform logging and telemetry settings."""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    format: Literal["json", "console"] = "json"
    enable_telemetry: bool = False


class LLMSettings(BaseModel):
    """LLM Gateway and provider configuration settings."""

    default_provider: str = "openai"
    default_model: str = "gpt-4o"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    request_timeout_seconds: int = Field(default=60, ge=1)
    max_retries: int = Field(default=3, ge=0)


class FeatureFlagSettings(BaseModel):
    """Experimental feature toggle flags."""

    enable_graph_rag: bool = True
    enable_agent_sandbox: bool = True
    enable_plugin_hot_reload: bool = False


class Settings(BaseSettings):
    """Root platform settings container loading from environment and .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        frozen=True,
    )

    app: AppSettings = Field(default_factory=AppSettings)
    runtime: RuntimeSettings = Field(default_factory=RuntimeSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    features: FeatureFlagSettings = Field(default_factory=FeatureFlagSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached immutable singleton Settings instance."""
    return Settings()
