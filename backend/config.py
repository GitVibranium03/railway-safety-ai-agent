"""
Configuration management for Railway Safety Agent
"""
import os
from typing import Dict, Any
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Model Settings
    MODEL_TYPE: str = "decision_tree"  # "decision_tree" or "logistic_regression"
    MODEL_TRAIN_ON_STARTUP: bool = True
    MODEL_CACHE_ENABLED: bool = True
    
    # Risk Thresholds
    RISK_THRESHOLD_LOW: float = 30.0
    RISK_THRESHOLD_MEDIUM: float = 60.0
    
    # Input Validation Ranges
    VISIBILITY_MIN: float = 0.0
    VISIBILITY_MAX: float = 10000.0
    SPEED_MIN: float = 0.0
    SPEED_MAX: float = 500.0
    WEATHER_OPTIONS: list = ["Clear", "Rain", "Fog"]
    
    # Feature Scaling
    VISIBILITY_SCALE_FACTOR: float = 10000.0
    SPEED_SCALE_FACTOR: float = 500.0
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "railway_safety.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Risk level labels
RISK_LABELS = ["Low", "Medium", "High"]

# Weather encoding mapping
WEATHER_ENCODING: Dict[str, int] = {
    "Clear": 0,
    "Rain": 1,
    "Fog": 2
}

# Reverse weather encoding
WEATHER_DECODING: Dict[int, str] = {v: k for k, v in WEATHER_ENCODING.items()}
