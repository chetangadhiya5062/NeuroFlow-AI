"""Platform configuration settings definitions using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    """Application metadata and environment settings."""

    name: str = "NeuroFlow AI"
    version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False


class RuntimeSettings(BaseModel):
    """Platform runtime execution settings."""

    max_concurrent_agents: int = Field(default=50, ge=1)
    max_concurrent_workflows: int = Field(default=100, ge=1)
    default_execution_timeout_seconds: int = Field(default=300, ge=1)
    enable_hot_reloading: bool = False


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

    provider: str = Field(default="mock", validation_alias="LLM_PROVIDER")
    default_provider: str = "mock"
    default_model: str = "gpt-4o"
    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, validation_alias="GEMINI_API_KEY")
    anthropic_api_key: str | None = Field(
        default=None, validation_alias="ANTHROPIC_API_KEY"
    )
    ollama_base_url: str = Field(
        default="http://localhost:11434", validation_alias="OLLAMA_BASE_URL"
    )
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
