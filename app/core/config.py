from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    mongodb_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openai_api_key: Optional[str] = None
    
    # CORS and Security
    allowed_origins: str = "*"
    rate_limit_per_minute: int = 100
    max_audio_file_size_mb: int = 50
    
    # Logging
    log_level: str = "INFO"
    log_to_file: bool = True
    log_to_console: bool = True
    
    # Database Pooling
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    
    # Frontend
    api_base_url: str = "http://localhost:8000"
    
    # Development
    debug: bool = False
    reload: bool = False
    
    model_config = {"env_file": ".env"}

settings = Settings()
