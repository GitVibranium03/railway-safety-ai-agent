"""
Streamlit frontend for Railway Safety Agent
Autonomous AI Agent – evaluator-ready UI
"""

import streamlit as st
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Railway Safety Agent",
    page_icon="🚆",
    layout="wide",
)

# -------------------- CSS --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Roboto', sans-serif;
}

.card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    margin-bottom: 1.5rem;
}

.risk-low {
    background: #d4edda;
    border-left: 6px solid #28a745;
    padding: 1.5rem;
    border-radius: 10px;
}
.risk-medium {
    background: #fff3cd;
    border-left: 6px solid #ffc107;
    padding: 1.5rem;
    border-radius: 10px;
}
.risk-high {
    background: #f8d7da;
    border-left: 6px solid #dc3545;
    padding: 1.5rem;
    border-radius: 10px;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    color: white;
}

.stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: bold;
    padding: 0.8rem;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# -------------------- AI AGENT LOGIC --------------------
def assess_risk(visibility: float, speed: float, weather: str) -> dict:
    """
    Autonomous AI Agent Decision Logic
    """

    risk_score = 0
    factors = {}

    # Visibility
    if visibility < 100:
        risk_score += 40
        factors["visibility"] = "Extremely low visibility"
    elif visibility < 500:
        risk_score += 30
        factors["visibility"] = "Poor visibility"
    elif visibility < 1000:
        risk_score += 20
        factors["visibility"] = "Moderate visibility"
    elif visibility < 2000:
        risk_score += 10
        factors["visibility"] = "Reduced visibility"
    else:
        factors["visibility"] = "Good visibility"

    # Speed
    if speed > 150:
        risk_score += 30
        factors["speed"] = "Very high speed"
    elif speed > 120:
        risk_score += 20
        factors["speed"] = "High speed"
    elif speed > 80:
        risk_score += 10
        factors["speed"] = "Moderate speed"
    else:
        factors["speed"] = "Safe speed"

    # Weather
    if weather == "Fog":
        risk_score += 30
        factors["weather"] = "Foggy conditions"
    elif weather == "Rain":
        risk_score += 15
        factors["weather"] = "Rainy conditions"
    else:
        factors["weather"] = "Clear weather"

    # Final decision
    if risk_score > 60:
        risk = "High"
        recommendation = (
            "🚨 EMERGENCY ACTION REQUIRED:\n"
            "- Reduce speed immediately\n"
            "- Alert control room\n"
            "- Consider temporary halt"
        )
    elif risk_score > 30:
        risk = "Medium"
        recommendation = (
            "⚠️ CAUTION ADVISED:\n"
            "- Reduce speed by 20–30 km/h\n"
            "- Increase crew alertness"
        )
    else:
        risk = "Low"
        recommendation = "✅ SAFE OPERATION:\n- Continue normal operation"

    return {
        "risk_level": risk,
        "risk_score": risk_score,
        "contributing_factors": factors,
        "recommendation": recommendation
    }

def risk_icon(risk: str) -> str:
    return {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(risk, "⚪")

# -------------------- MAIN APP --------------------
def main():

    # -------- SESSION STATE --------
    if "agent_state" not in st.session_state:
        st.session_state.agent_state = "Monitoring"

    if "decision_history" not in st.session_state:
        st.session_state.decision_history = []

    if "risk_trend" not in st.session_state:
        st.session_state.risk_trend = []

    if "last_risk" not in st.session_state:
        st.session_state.last_risk = "Unknown"

    if "last_eval_time" not in st.session_state:
        st.session_state.last_eval_time = 0

    # -------------------- SIDEBAR --------------------
    with st.sidebar:
        st.markdown("## 🤖 AI Agent Control Panel")
        st.markdown("### 🚦 Agent State")
        st.markdown(f"{risk_icon(st.session_state.last_risk)} **{st.session_state.agent_state}**")

        st.markdown("---")
        st.markdown("### 🧠 Decision Memory")
        if st.session_state.decision_history:
            for d in st.session_state.decision_history:
                st.markdown(f"- {d}")
        else:
            st.markdown("_No decisions yet_")

        st.markdown("---")
        st.markdown("🎯 **Agent Objectives**")
        st.markdown("- Prevent accidents")
        st.markdown("- Prioritize passenger safety")
        st.markdown("- Act autonomously")

    # -------------------- MAIN UI --------------------
    st.markdown("## 🚆 Railway Safety Agent")
    st.caption(
        "An autonomous AI agent that continuously observes, evaluates, and acts for railway safety."
    )

    col1, col2 = st.columns(2)

    # -------- ENVIRONMENT INPUT --------
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🌍 Environment Observation")

        visibility = st.slider("👁 Visibility (meters)", 0, 10000, 3000, step=50)
        speed = st.slider("⚡ Train Speed (km/h)", 0, 500, 120, step=5)
        weather = st.selectbox("🌦 Weather Condition", ["Clear", "Rain", "Fog"])

        agent_active = st.toggle("🤖 Autonomous Mode", value=False)
        manual_eval = st.button("🔄 Manual Evaluation Cycle", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- AGENT DECISION --------
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🧠 Agent Decision & Action")

        run_agent = manual_eval or agent_active

        if agent_active and time.time() - st.session_state.last_eval_time > 5:
            st.session_state.last_eval_time = time.time()
            run_agent = True

        if run_agent:
            with st.spinner("🤖 Agent evaluating environment..."):
                result = assess_risk(visibility, speed, weather)

            risk = result["risk_level"]
            st.session_state.last_risk = risk

            if risk == "High":
                st.session_state.agent_state = "Alerting"
            elif risk == "Medium":
                st.session_state.agent_state = "Evaluating"
            else:
                st.session_state.agent_state = "Monitoring"

            st.session_state.decision_history.insert(
                0, f"{risk} | {weather}, {speed} km/h"
            )
            st.session_state.decision_history = st.session_state.decision_history[:5]

            st.session_state.risk_trend.append(risk)
            st.session_state.risk_trend = st.session_state.risk_trend[-10:]

            if risk == "Low":
                st.markdown('<div class="risk-low"><h2>🟢 LOW RISK</h2></div>', unsafe_allow_html=True)
            elif risk == "Medium":
                st.markdown('<div class="risk-medium"><h2>🟡 MEDIUM RISK</h2></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="risk-high"><h2>🔴 HIGH RISK</h2></div>', unsafe_allow_html=True)

            st.markdown("#### 🔍 Agent Explanation")
            st.json(result["contributing_factors"])

            st.markdown("#### 🎯 Agent Recommendation")
            st.info(result["recommendation"])

            if agent_active:
                st.experimental_rerun()
        else:
            st.info("Agent is monitoring. Enable autonomous mode or trigger manual evaluation.")

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- RISK TREND --------
    if st.session_state.risk_trend:
        st.markdown("### 📈 Risk Trend")
        trend_map = {"Low": 1, "Medium": 2, "High": 3}
        st.line_chart([trend_map[r] for r in st.session_state.risk_trend])

    # -------- FOOTER --------
    st.markdown("---")
    st.markdown(
        "<center><strong>Railway Safety Agent</strong> | Autonomous AI System | SDG 11</center>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
