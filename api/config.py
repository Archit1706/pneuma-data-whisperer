from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Pneuma Configuration
    pneuma_storage_path: str = "./storage"
    pneuma_llm_path: str = "Qwen/Qwen2.5-7B-Instruct"
    pneuma_embed_path: str = "BAAI/bge-base-en-v1.5"
    pneuma_default_index: str = "default"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    api_log_level: str = "info"

    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    # Session Management
    session_expire_hours: int = 24
    secret_key: str = "change-this-in-production"

    # OpenWebUI Configuration (optional fields)
    openwebui_host: str = "localhost"
    openwebui_port: int = 8080
    ollama_base_url: str = "http://localhost:11434"

    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090

    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow extra fields that might be in .env
        extra = "ignore"


settings = Settings()