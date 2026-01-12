# 🚆 Railway Safety Agent – Autonomous AI System

An **autonomous AI agent** designed to assist railway operators by continuously
observing operational and environmental conditions, evaluating accident risk,
and recommending safety actions.

This project aligns with **SDG 11: Sustainable Cities & Communities** by promoting
safer and more reliable transportation systems.

---

## 🧠 Key Capabilities

- Autonomous AI agent (observe → decide → act)
- ML-based risk prediction (Decision Tree / Logistic Regression)
- Agent state & decision memory
- Explainable safety recommendations
- Human-in-the-loop manual override
- Interactive Streamlit dashboard
- Fully tested backend logic (pytest)

---

## 🤖 Why This Is an AI Agent (Not Just ML)

Unlike traditional machine learning applications that respond only to user input,
this system implements an **autonomous agent** that:

- Continuously observes the environment
- Maintains internal state and recent decision history
- Evaluates risk independently using a learned model
- Explains its reasoning
- Recommends actions based on safety objectives

This agent-based design reflects modern applied AI system architecture.

---

## 🏗️ System Architecture

### Frontend
- **Streamlit**
- Monitoring dashboard for observed environment and agent decisions
- Live risk status, decision history, and trend visualization

### Backend
- **FastAPI** REST API
- Custom AI agent logic (LangGraph-compatible design)
- Hybrid AI approach (machine learning + rule-based safety logic)

### AI & ML
- **Scikit-learn** models for risk estimation
- Explainable decision outputs
- Safety-first decision policies

### Testing
- **Pytest**
- Unit tests for agent behavior, validation, and ML logic

---

## 🚀 How to Run the Project

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
    2️⃣ Start Backend Server
    uvicorn backend.main:app --reload
      Backend runs at:
      http://localhost:8000 
    3️⃣ Start Frontend  Backend runs at:
      streamlit run frontend.py
      http://localhost:8501
      
