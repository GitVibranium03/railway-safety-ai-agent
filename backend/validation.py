"""
Centralized input validation logic
"""
from typing import Optional, Tuple, List
from pydantic import ValidationError
import logging
from backend.config import settings
from backend.models import SafetyInput

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_inputs(
    visibility: Optional[float],
    speed: Optional[float],
    weather: Optional[str]
) -> Tuple[bool, List[str], Optional[SafetyInput]]:
    """
    Validate all input parameters.
    
    Args:
        visibility: Visibility in meters
        speed: Speed in km/h
        weather: Weather condition
    
    Returns:
        Tuple of (is_valid, missing_fields, validated_input)
    """
    missing_fields = []
    
    # Check for missing values
    if visibility is None:
        missing_fields.append("visibility")
    if speed is None:
        missing_fields.append("speed")
    if weather is None:
        missing_fields.append("weather")
    
    if missing_fields:
        return False, missing_fields, None
    
    # Validate types and ranges
    try:
        validated_input = SafetyInput(
            visibility=visibility,
            speed=speed,
            weather=weather
        )
        
        # Additional custom validations
        errors = []
        
        # Check for negative or zero values
        if validated_input.visibility is not None:
            if validated_input.visibility <= 0:
                errors.append("Visibility must be greater than 0")
            if validated_input.visibility > settings.VISIBILITY_MAX:
                errors.append(f"Visibility exceeds maximum ({settings.VISIBILITY_MAX}m)")
        
        if validated_input.speed is not None:
            if validated_input.speed <= 0:
                errors.append("Speed must be greater than 0")
            if validated_input.speed > settings.SPEED_MAX:
                errors.append(f"Speed exceeds maximum ({settings.SPEED_MAX} km/h)")
        
        if validated_input.weather is not None:
            if validated_input.weather not in settings.WEATHER_OPTIONS:
                errors.append(f"Weather must be one of: {', '.join(settings.WEATHER_OPTIONS)}")
        
        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise ValueError("; ".join(errors))
        
        return True, [], validated_input
        
    except ValidationError as e:
        logger.error(f"Pydantic validation error: {e}")
        return False, ["Invalid input format"], None
    except ValueError as e:
        logger.error(f"Value validation error: {e}")
        return False, [str(e)], None
    except Exception as e:
        logger.error(f"Unexpected validation error: {e}")
        return False, ["Unexpected validation error"], None


def validate_numeric_range(
    value: float, 
    min_val: float, 
    max_val: float, 
    field_name: str
) -> bool:
    """Validate numeric value is within range"""
    if value < min_val or value > max_val:
        raise ValueError(f"{field_name} must be between {min_val} and {max_val}")
    return True


def validate_weather(weather: str) -> bool:
    """Validate weather condition"""
    if weather not in settings.WEATHER_OPTIONS:
        raise ValueError(f"Weather must be one of: {', '.join(settings.WEATHER_OPTIONS)}")
    return True
