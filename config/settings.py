"""
Configuration module for Cynbit AI Pre-Sales Solution Architect.
Reads environment variables safely using pydantic-settings.
"""

from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment fallback."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM Settings
    llm_provider: Literal["gemini", "openai", "offline"] = Field(
        default="gemini",
        alias="LLM_PROVIDER",
        description="Active LLM provider. Falls back to offline if keys missing.",
    )
    gemini_api_key: Optional[str] = Field(
        default=None,
        alias="GEMINI_API_KEY",
        description="Google Gemini API Key",
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        alias="OPENAI_API_KEY",
        description="OpenAI API Key",
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash",
        alias="GEMINI_MODEL",
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        alias="OPENAI_MODEL",
    )

    # Financial & Estimation Defaults
    default_hourly_cost: float = Field(
        default=45.0,
        alias="DEFAULT_HOURLY_COST",
        description="Internal cost per developer/specialist hour in USD",
    )
    default_hourly_bill_rate: float = Field(
        default=95.0,
        alias="DEFAULT_HOURLY_BILL_RATE",
        description="Standard client billing rate in USD",
    )
    default_target_margin_pct: float = Field(
        default=35.0,
        alias="DEFAULT_TARGET_MARGIN_PCT",
        description="Default target profit margin percentage",
    )
    default_contingency_pct: float = Field(
        default=15.0,
        alias="DEFAULT_CONTINGENCY_PCT",
        description="Contingency buffer percentage for unknowns",
    )

    # Document Ingestion limits
    max_file_size_mb: int = Field(default=10, description="Max uploaded brief size")
    allowed_extensions: list[str] = Field(default=["pdf", "docx", "txt", "md"])

    # General
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


settings = Settings()
