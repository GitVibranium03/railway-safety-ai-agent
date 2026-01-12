"""
Data models for railway safety agent
"""
from typing import Optional, Literal, TypedDict
from pydantic import BaseModel, Field


class SafetyInput(BaseModel):
    """Input parameters for risk assessment"""
    visibility: Optional[float] = Field(None, ge=0, le=10000, description="Visibility in meters")
    speed: Optional[float] = Field(None, ge=0, le=500, description="Train speed in km/h")
    weather: Optional[Literal["Clear", "Rain", "Fog"]] = Field(None, description="Weather condition")


class ContributingFactors(BaseModel):
    """Contributing factors for risk assessment"""
    visibility_contribution: float = Field(0.0, ge=0.0, le=1.0)
    speed_contribution: float = Field(0.0, ge=0.0, le=1.0)
    weather_contribution: float = Field(0.0, ge=0.0, le=1.0)


class SafetyOutput(BaseModel):
    """Output from safety agent with explainability"""
    risk_level: Literal["Low", "Medium", "High"]
    alert_message: str
    recommendation: str
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Model confidence score")
    contributing_factors: Optional[ContributingFactors] = None
    missing_inputs: Optional[list[str]] = None


class AgentState(TypedDict):
    """State passed between LangGraph nodes (TypedDict for LangGraph compatibility)"""
    visibility: Optional[float]
    speed: Optional[float]
    weather: Optional[str]
    missing_inputs: list[str]
    risk_score: Optional[float]
    risk_level: Optional[str]
    alert_message: Optional[str]
    recommendation: Optional[str]
    needs_clarification: bool
    confidence: Optional[float]
    contributing_factors: Optional[dict]