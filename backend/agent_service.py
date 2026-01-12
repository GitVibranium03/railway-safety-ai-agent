"""
Agent service with explicit perceive(), decide(), act() methods
"""
from typing import Dict, Any, Optional
import logging
from backend.models import AgentState
from backend.validation import validate_inputs
from backend.ml_model import get_model
from backend.config import settings

logger = logging.getLogger(__name__)


class RailwaySafetyAgent:
    """Autonomous AI agent for railway safety assessment"""
    
    def __init__(self):
        """Initialize the agent"""
        self.model = get_model()
    
    def perceive(self, inputs: Dict[str, Any]) -> AgentState:
        """
        Perceive the environment - validate and process inputs.
        
        Args:
            inputs: Dictionary with visibility, speed, weather
        
        Returns:
            AgentState with perceived information
        """
        visibility = inputs.get("visibility")
        speed = inputs.get("speed")
        weather = inputs.get("weather")
        
        # Validate inputs
        is_valid, missing_fields, validated_input = validate_inputs(
            visibility, speed, weather
        )
        
        # Create initial state
        state: AgentState = {
            "visibility": visibility,
            "speed": speed,
            "weather": weather,
            "missing_inputs": missing_fields,
            "risk_score": None,
            "risk_level": None,
            "alert_message": None,
            "recommendation": None,
            "needs_clarification": not is_valid,
            "confidence": None,
            "contributing_factors": None
        }
        
        return state
    
    def decide(self, state: AgentState) -> AgentState:
        """
        Make autonomous decision based on perceived state.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with decision
        """
        if state.get("needs_clarification"):
            logger.info("Decision skipped - missing inputs")
            return state
        
        try:
            # Use ML model for prediction
            risk_level, confidence, contributing_factors = self.model.predict_risk(
                visibility=state["visibility"],
                speed=state["speed"],
                weather=state["weather"]
            )
            
            state["risk_level"] = risk_level
            state["confidence"] = confidence
            state["contributing_factors"] = contributing_factors
            
            logger.info(f"Decision made: {risk_level} risk (confidence: {confidence:.2f})")
            
        except Exception as e:
            logger.error(f"Error in decision making: {e}")
            state["risk_level"] = "Medium"  # Default to medium on error
            state["confidence"] = 0.5
            state["contributing_factors"] = {}
        
        return state
    
    def act(self, state: AgentState) -> AgentState:
        """
        Act on the decision - generate alerts and recommendations.
        
        Args:
            state: Current agent state with decision
        
        Returns:
            Updated state with actions
        """
        if state.get("needs_clarification"):
            missing_str = ", ".join(state.get("missing_inputs", []))
            state["alert_message"] = (
                f"Missing required safety parameters: {missing_str}. "
                "Please provide the missing information to proceed with risk assessment."
            )
            state["recommendation"] = f"Please provide the following parameter(s): {missing_str}"
            return state
        
        risk_level = state.get("risk_level")
        if risk_level is None:
            state["alert_message"] = "Unable to assess risk. Please check inputs."
            state["recommendation"] = "Verify all parameters are correct."
            return state
        
        # Generate alerts and recommendations based on risk level
        confidence = state.get("confidence", 0.0)
        factors = state.get("contributing_factors", {})
        
        if risk_level == "Low":
            state["alert_message"] = "✅ SAFE OPERATING CONDITIONS DETECTED"
            state["recommendation"] = (
                "Current operational parameters indicate safe conditions. "
                "Maintain normal operations with standard vigilance. "
                "Continue monitoring visibility, speed, and weather conditions."
            )
        
        elif risk_level == "Medium":
            state["alert_message"] = "⚠️ CAUTION ALERT: ELEVATED RISK CONDITIONS"
            state["recommendation"] = (
                "Moderate risk detected. Recommended actions:\n"
                "- Reduce train speed by 20-30 km/h\n"
                "- Increase alertness and monitoring\n"
                "- Notify control room of current conditions\n"
                "- Prepare for potential further speed reduction if conditions worsen"
            )
        
        elif risk_level == "High":
            state["alert_message"] = "🚨 EMERGENCY WARNING: HIGH RISK CONDITIONS"
            state["recommendation"] = (
                "HIGH RISK detected. IMMEDIATE ACTION REQUIRED:\n"
                "- Reduce speed immediately to safe operational limits (≤60 km/h recommended)\n"
                "- Alert control room and dispatch immediately\n"
                "- Increase crew alertness to maximum level\n"
                "- Consider temporary halt if visibility drops below 100m\n"
                "- Activate emergency protocols if conditions deteriorate further"
            )
        
        # Add explainability information to recommendation
        if factors:
            factor_explanation = self._format_contributing_factors(factors)
            state["recommendation"] += f"\n\nContributing Factors:\n{factor_explanation}"
        
        return state
    
    def _format_contributing_factors(self, factors: Dict[str, float]) -> str:
        """Format contributing factors for display"""
        lines = []
        if factors.get("visibility_contribution", 0) > 0.1:
            lines.append(f"- Visibility: {factors['visibility_contribution']:.1%} contribution")
        if factors.get("speed_contribution", 0) > 0.1:
            lines.append(f"- Speed: {factors['speed_contribution']:.1%} contribution")
        if factors.get("weather_contribution", 0) > 0.1:
            lines.append(f"- Weather: {factors['weather_contribution']:.1%} contribution")
        
        return "\n".join(lines) if lines else "All factors contribute equally"
    
    def process(self, inputs: Dict[str, Any]) -> AgentState:
        """
        Complete agent workflow: perceive -> decide -> act
        
        Args:
            inputs: Input parameters
        
        Returns:
            Final agent state
        """
        state = self.perceive(inputs)
        state = self.decide(state)
        state = self.act(state)
        return state


# Global agent instance
_agent_instance: Optional[RailwaySafetyAgent] = None


def get_agent() -> RailwaySafetyAgent:
    """Get or create the global agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = RailwaySafetyAgent()
    return _agent_instance
