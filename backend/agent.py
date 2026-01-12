"""
LangGraph agent workflow for railway safety decision-making
"""
from typing import Literal
from langgraph.graph import StateGraph, END
from backend.models import AgentState
from backend.risk_analyzer import calculate_risk_score, classify_risk_level


def start_node(state: AgentState) -> AgentState:
    """
    Initial node: Validate inputs and check for missing parameters.
    """
    missing = []
    
    if state.get("visibility") is None:
        missing.append("visibility")
    if state.get("speed") is None:
        missing.append("speed")
    if state.get("weather") is None:
        missing.append("weather")
    
    state["missing_inputs"] = missing
    state["needs_clarification"] = len(missing) > 0
    
    return state


def risk_analyzer_node(state: AgentState) -> AgentState:
    """
    Analyze operational parameters and calculate risk score.
    """
    if state.get("needs_clarification"):
        # Skip risk analysis if inputs are missing
        return state
    
    risk_score = calculate_risk_score(
        state.get("visibility"),
        state.get("speed"),
        state.get("weather")
    )
    
    state["risk_score"] = risk_score
    return state


def decision_node(state: AgentState) -> AgentState:
    """
    Classify risk level based on calculated risk score.
    """
    if state.get("needs_clarification") or state.get("risk_score") is None:
        return state
    
    state["risk_level"] = classify_risk_level(state["risk_score"])
    return state


def alert_node(state: AgentState) -> AgentState:
    """
    Generate safety alerts and recommendations based on risk level.
    """
    if state.get("needs_clarification"):
        # Generate clarification message
        missing_str = ", ".join(state.get("missing_inputs", []))
        state["alert_message"] = f"Missing required safety parameters: {missing_str}. Please provide the missing information to proceed with risk assessment."
        state["recommendation"] = f"Please provide the following parameter(s): {missing_str}"
        state["risk_level"] = None
        return state
    
    risk_level = state.get("risk_level")
    if risk_level is None:
        return state
    
    # Generate alerts and recommendations based on risk level
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
    
    return state


def build_safety_agent() -> StateGraph:
    """
    Build and return the LangGraph agent workflow.
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("start", start_node)
    workflow.add_node("risk_analyzer", risk_analyzer_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("alert", alert_node)
    
    # Define edges
    workflow.set_entry_point("start")
    workflow.add_edge("start", "risk_analyzer")
    workflow.add_edge("risk_analyzer", "decision")
    workflow.add_edge("decision", "alert")
    workflow.add_edge("alert", END)
    
    return workflow.compile()
