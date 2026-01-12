"""
Service layer for railway safety agent
Separates business logic from API routes
"""
import logging
from typing import Dict, Any
from backend.agent_service import get_agent
from backend.models import SafetyInput, SafetyOutput, ContributingFactors
from backend.validation import validate_inputs

logger = logging.getLogger(__name__)


class RiskAssessmentService:
    """Service for risk assessment operations"""
    
    def __init__(self):
        """Initialize the service"""
        self.agent = get_agent()
    
    def assess_risk(self, input_data: SafetyInput) -> SafetyOutput:
        """
        Assess risk using the agent.
        
        Args:
            input_data: Safety input parameters
        
        Returns:
            SafetyOutput with risk assessment and explainability
        """
        try:
            # Convert Pydantic model to dict
            inputs = {
                "visibility": input_data.visibility,
                "speed": input_data.speed,
                "weather": input_data.weather
            }
            
            # Process through agent
            state = self.agent.process(inputs)
            
            # Handle missing inputs
            if state.get("needs_clarification"):
                return SafetyOutput(
                    risk_level="Low",  # Default placeholder
                    alert_message=state.get("alert_message") or "Missing required parameters",
                    recommendation=state.get("recommendation") or "Please provide all required parameters",
                    missing_inputs=state.get("missing_inputs", []),
                    confidence=None,
                    contributing_factors=None
                )
            
            # Extract contributing factors
            factors_dict = state.get("contributing_factors", {})
            contributing_factors = None
            if factors_dict:
                contributing_factors = ContributingFactors(
                    visibility_contribution=factors_dict.get("visibility_contribution", 0.0),
                    speed_contribution=factors_dict.get("speed_contribution", 0.0),
                    weather_contribution=factors_dict.get("weather_contribution", 0.0)
                )
            
            # Return structured output with explainability
            return SafetyOutput(
                risk_level=state.get("risk_level") or "Low",
                alert_message=state.get("alert_message") or "Risk assessment completed",
                recommendation=state.get("recommendation") or "Continue monitoring conditions",
                confidence=state.get("confidence"),
                contributing_factors=contributing_factors,
                missing_inputs=None
            )
            
        except Exception as e:
            logger.error(f"Error in risk assessment service: {e}", exc_info=True)
            raise


# Global service instance
_service_instance = None


def get_service() -> RiskAssessmentService:
    """Get or create the global service instance"""
    global _service_instance
    if _service_instance is None:
        _service_instance = RiskAssessmentService()
    return _service_instance
