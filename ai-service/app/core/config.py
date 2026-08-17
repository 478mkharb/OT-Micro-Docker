from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    environment: str
    log_level: str

    host: str
    port: int

    ollama_base_url: str
    ollama_model: str
    ollama_timeout: int

    prometheus_url: str
    prometheus_timeout: int
    tempo_url: str
    loki_url: str
    loki_timeout: int
    
    api_prefix: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()