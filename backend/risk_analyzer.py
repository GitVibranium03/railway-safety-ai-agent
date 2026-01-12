"""
AI-based risk analysis logic for railway safety
"""
from typing import Optional


def calculate_risk_score(visibility: Optional[float], speed: Optional[float], weather: Optional[str]) -> float:
    """
    Calculate risk score based on operational parameters.
    Returns a score between 0 (lowest risk) and 100 (highest risk).
    
    Risk factors:
    - Low visibility increases risk
    - High speed increases risk
    - Adverse weather (Fog > Rain > Clear) increases risk
    """
    if visibility is None or speed is None or weather is None:
        return 0.0
    
    risk_score = 0.0
    
    # Visibility factor (0-40 points)
    # Lower visibility = higher risk
    if visibility < 100:
        visibility_risk = 40
    elif visibility < 500:
        visibility_risk = 30
    elif visibility < 1000:
        visibility_risk = 20
    elif visibility < 2000:
        visibility_risk = 10
    else:
        visibility_risk = 0
    
    risk_score += visibility_risk
    
    # Speed factor (0-30 points)
    # Higher speed = higher risk
    if speed > 150:
        speed_risk = 30
    elif speed > 120:
        speed_risk = 20
    elif speed > 80:
        speed_risk = 10
    else:
        speed_risk = 0
    
    risk_score += speed_risk
    
    # Weather factor (0-30 points)
    weather_risk_map = {
        "Clear": 0,
        "Rain": 15,
        "Fog": 30
    }
    risk_score += weather_risk_map.get(weather, 0)
    
    # Combined risk multiplier for dangerous combinations
    if weather == "Fog" and visibility < 200:
        risk_score *= 1.3  # Severe visibility issue
    if speed > 120 and visibility < 500:
        risk_score *= 1.2  # High speed + low visibility
    
    return min(risk_score, 100.0)


def classify_risk_level(risk_score: float) -> str:
    """
    Classify risk score into Low, Medium, or High risk categories.
    """
    if risk_score < 30:
        return "Low"
    elif risk_score < 60:
        return "Medium"
    else:
        return "High"
