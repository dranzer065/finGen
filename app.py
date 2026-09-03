import os
import streamlit as st
from dotenv import load_dotenv

# Load environment secrets
load_dotenv()

from src.main import run_fingen

st.set_page_config(page_title="finGen - Wealth Engine", page_icon="📈", layout="wide")

st.title("finGen: Autonomous Multi-Agent Wealth Engine")
st.caption("Deterministic cash-flow modeling + real-time benchmark search powered by Gemini & CrewAI.")

# Sidebar Configuration
with st.sidebar:
    st.header("Financial Profile")
    
    age = st.number_input("Age", min_value=18, max_value=70, value=25, step=1)
    monthly_income = st.number_input("Monthly Income (₹)", min_value=1000, value=75000, step=5000)
    monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=0, value=30000, step=2500)
    current_savings = st.number_input("Current Liquid Savings (₹)", min_value=0, value=50000, step=5000)
    existing_debts = st.number_input("High-Interest Debts (₹)", min_value=0, value=0, step=5000)
    risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"], index=1)
    
    st.divider()
    
    gemini_key = st.text_input("Gemini API Key (optional override)", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    tavily_key = st.text_input("Tavily API Key (optional override)", type="password", value=os.getenv("TAVILY_API_KEY", ""))
    
    generate_btn = st.button("Generate Strategy Roadmap", type="primary", use_container_width=True)

# Main Output Panel
if generate_btn:
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key
        
    if not os.getenv("GEMINI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        st.error("Please supply valid GEMINI_API_KEY and TAVILY_API_KEY credentials.")
    else:
        profile_data = {
            "age": age,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "current_savings": current_savings,
            "existing_debts": existing_debts,
            "risk_tolerance": risk_tolerance
        }
        
        with st.status("Agents collaborating: Profiling -> Researching -> Formulating Strategy...", expanded=True) as status:
            st.write("🔍 Profiling cash-flow and determining risk boundaries...")
            try:
                result = run_fingen(profile_data)
                status.update(label="Strategy Roadmap Formulated Successfully!", state="complete", expanded=False)
                
                st.subheader("Your Generated Wealth Roadmap")
                st.markdown(result)
            except Exception as e:
                status.update(label="Execution Failed", state="error")
                st.error(f"Error during agent pipeline execution: {str(e)}")
else:
    st.info("Adjust the parameters in the left sidebar and click **Generate Strategy Roadmap** to run your multi-agent crew.")