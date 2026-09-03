import os
import streamlit as st
from dotenv import load_dotenv

# Load local environment secrets
load_dotenv()

from src.main import run_fingen_pipeline

st.set_page_config(
    page_title="finGen • Autonomous Wealth Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FinTech UI Styling: High-contrast Gradients, Glassmorphic Cards, News Radar
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 20% 10%, rgba(16, 185, 129, 0.08) 0%, rgba(11, 15, 23, 1) 50%);
        color: #F8FAFC;
    }

    /* Brand Logo & Title Styling */
    .brand-container {
        padding: 1.2rem 0 0.8rem 0;
        margin-bottom: 1.5rem;
    }
    .brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.12);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .brand-logo {
        font-size: 3.4rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.1;
        background: linear-gradient(135deg, #10B981 0%, #06B6D4 45%, #6366F1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
        filter: drop-shadow(0 4px 18px rgba(6, 182, 212, 0.25));
    }
    .brand-tagline {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-top: 0.4rem;
    }

    /* Section Labels */
    .section-label {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748B;
        margin-bottom: 0.8rem;
    }

    /* 4-Box News Intelligence Grid */
    .news-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.85rem;
        margin-bottom: 2rem;
    }
    .news-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .news-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        transform: translateY(-2px);
        background: rgba(22, 32, 54, 0.8);
    }
    .news-tag {
        font-size: 0.7rem;
        font-weight: 700;
        color: #06B6D4;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .news-headline {
        font-size: 0.88rem;
        font-weight: 600;
        color: #E2E8F0;
        line-height: 1.35;
        margin-bottom: 0.5rem;
    }
    .news-impact {
        font-size: 0.72rem;
        color: #94A3B8;
        font-weight: 400;
    }

    /* Metric Cards Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(180deg, rgba(22, 30, 48, 0.7) 0%, rgba(13, 19, 32, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.25rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .metric-label {
        color: #64748B;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }
    .metric-footnote {
        font-size: 0.75rem;
        color: #10B981;
        margin-top: 0.3rem;
        font-weight: 500;
    }
    .metric-alert {
        color: #F59E0B;
    }

    /* Sidebar Theme */
    section[data-testid="stSidebar"] {
        background-color: #0A0E17 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    section[data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }

    /* Action Button Gradient */
    div.stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #06B6D4 50%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 1.6rem !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3) !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 6px 28px rgba(6, 182, 212, 0.5) !important;
        transform: translateY(-2px) !important;
    }

    .report-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 14px;
        padding: 2.2rem;
        margin-top: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# 1. Sidebar Inputs
with st.sidebar:
    st.markdown("<h3 style='color:#FFF; font-weight:800; margin-bottom:1rem;'>Parameters</h3>", unsafe_allow_html=True)
    
    age = st.number_input("Age", min_value=18, max_value=65, value=20, step=1)
    status = st.selectbox(
        "Employment Status",
        [
            "Active Earner / Freelancer",
            "College Student (Part-Time)",
            "Salaried Professional (Early Career)",
            "Full-Time Student"
        ]
    )
    
    monthly_income = st.number_input("Monthly Income (₹)", min_value=1000, value=5000, step=500)
    monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=500, value=3000, step=500)
    current_savings = st.number_input("Current Liquid Savings (₹)", min_value=0, value=1500, step=500)
    existing_debts = st.number_input("High-Interest Debts (₹)", min_value=0, value=0, step=500)
    
    time_horizon = st.slider("Horizon (Years)", min_value=3, max_value=30, value=10)
    risk_level = st.selectbox(
        "Risk Posture",
        ["Conservative", "Moderate Growth", "Aggressive Equity"],
        index=2
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.button("⚡ Formulate Wealth Roadmap", use_container_width=True)

# 2. Hero Section
st.markdown("""
<div class="brand-container">
    <div class="brand-badge">⚡ Autonomous Wealth Intelligence</div><br>
    <div class="brand-logo">finGen</div>
    <div class="brand-tagline">Deterministic cash-flow modeling paired with live market benchmarking via Google Gemini & CrewAI.</div>
</div>
""", unsafe_allow_html=True)

# 3. Market Intelligence News Radar (4 Boxes)
st.markdown('<div class="section-label">Real-Time Market Radar</div>', unsafe_allow_html=True)
st.markdown("""
<div class="news-grid">
    <div class="news-card">
        <div>
            <div class="news-tag">Broad Indices</div>
            <div class="news-headline">Nifty 50 & S&P 500 Index Funds Inflow Reaches New All-Time High</div>
        </div>
        <div class="news-impact">Passive ETF expense ratios drop to record low 0.03%.</div>
    </div>
    <div class="news-card">
        <div>
            <div class="news-tag">Macro Rates</div>
            <div class="news-headline">Central Banks Signal Neutral Rate Stance Amid Cooling Core Inflation</div>
        </div>
        <div class="news-impact">Yields stabilize; ideal climate for dollar-cost averaging.</div>
    </div>
    <div class="news-card">
        <div>
            <div class="news-tag">Youth Finance</div>
            <div class="news-headline">Regulatory Reports Show 93% F&O Retail Traders Incur Net Losses</div>
        </div>
        <div class="news-impact">Advisors advocate broad equity indexing over derivatives.</div>
    </div>
    <div class="news-card">
        <div>
            <div class="news-tag">Compounding Trends</div>
            <div class="news-headline">Systematic SIP Volumes Cross Milestone Among Early-Career Earners</div>
        </div>
        <div class="news-impact">Early compounding adoption creates significant 10-year runways.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Math computations
surplus = max(0, monthly_income - monthly_expenses)
emergency_target = monthly_expenses * 6
deficit = max(0, emergency_target - current_savings)

# 4. Instant Metric Grid
st.markdown('<div class="section-label">Deterministic Portfolio Posture</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Monthly Surplus</div>
        <div class="metric-value">₹{surplus:,.0f}</div>
        <div class="metric-footnote">Surplus ready for deployment</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Emergency Reserve Target</div>
        <div class="metric-value">₹{emergency_target:,.0f}</div>
        <div class="metric-footnote">6-month baseline protection</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Reserve Deficit</div>
        <div class="metric-value">₹{deficit:,.0f}</div>
        <div class="metric-footnote {'metric-alert' if deficit > 0 else ''}">{'Priority funding phase' if deficit > 0 else 'Reserve fully secured'}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Compounding Window</div>
        <div class="metric-value">{time_horizon} Years</div>
        <div class="metric-footnote">Long-term investment horizon</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Live Multi-Agent Execution Pipeline
if submit_btn:
    user_payload = {
        "age": age,
        "status": status,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "monthly_savings": surplus,
        "current_savings": current_savings,
        "existing_debts": existing_debts,
        "time_horizon_years": time_horizon,
        "risk_level": risk_level
    }

    report_container = st.container()

    with st.status("Executing Multi-Agent Collaborative Analysis...", expanded=True) as status_box:
        st.write("🔍 **Youth Profiler:** Analyzing cash-flow surplus and emergency reserve runway...")
        st.write("📊 **Market Researcher:** Verifying benchmark index fees and real-time market metrics...")
        st.write("📑 **Wealth Strategist:** Formulating multi-horizon educational wealth roadmap...")
        
        try:
            roadmap = run_fingen_pipeline(user_payload)
            status_box.update(label="Strategy Roadmap Synthesized Successfully!", state="complete", expanded=False)
        except Exception as e:
            status_box.update(label="Pipeline Failed", state="error")
            st.error(f"Error during agent pipeline execution: {str(e)}")
            roadmap = None

    if roadmap:
        with report_container:
            st.markdown("### Synthesized Educational Wealth Roadmap")
            st.markdown(roadmap)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Wealth Roadmap (.md)",
                data=str(roadmap),
                file_name=f"finGen_roadmap_{age}yo.md",
                mime="text/markdown",
                use_container_width=True
            )
else:
    st.info("👈 Set your financial parameters on the left and click **Formulate Wealth Roadmap** to execute the pipeline.")