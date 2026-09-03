"""
finGen - Main Multi-Agent Execution Pipeline
Powered by Google Gemini & CrewAI.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure root folder is always in python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from crewai import Crew, Task, Process, LLM
from src.agents.profiler import create_profiler_agent
from src.agents.researcher import create_researcher_agent
from src.agents.strategist import create_strategist_agent
from src.core.calculators import calculate_sip, calculate_emergency_fund_target

# Load environment variables
load_dotenv()

# Verify API Keys
gemini_key = os.getenv("GEMINI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

if not gemini_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file! Please add it.")
if not tavily_key:
    raise ValueError("Missing TAVILY_API_KEY in .env file! Please add it.")

# Set keys in os.environ for underlying LiteLLM/Google SDK
os.environ["GEMINI_API_KEY"] = gemini_key
os.environ["GOOGLE_API_KEY"] = gemini_key

# Initialize CrewAI native LLM with the supported canonical model
gemini_llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=gemini_key,
    temperature=0.4
)


def run_fingen_pipeline(user_data: dict) -> str:
    print("\n" + "=" * 50)
    print("🚀 Running finGen Wealth Engine...")
    print("=" * 50 + "\n")

    # 1. Deterministic Financial Math (Pure Python - No Hallucinations)
    income = float(user_data.get("monthly_income", 15000))
    monthly_expenses = float(user_data.get("monthly_expenses", 8000))
    
    # Calculate savings capacity if not directly provided
    default_savings = max(0.0, income - monthly_expenses)
    monthly_savings = float(user_data.get("monthly_savings", default_savings))
    
    years = int(user_data.get("time_horizon_years", 10))
    expected_return = 12.0  # Historical equity index baseline (12% CAGR)

    sip_projections = calculate_sip(
        monthly_investment=monthly_savings,
        annual_return_rate=expected_return,
        years=years
    )

    emergency_target = calculate_emergency_fund_target(
        monthly_expenses=monthly_expenses,
        months_coverage=6
    )

    financial_context = (
        f"User Profile:\n"
        f"- Age: {user_data.get('age', 22)}\n"
        f"- Employment / Status: {user_data.get('status', 'Active Earner')}\n"
        f"- Monthly Income: ₹{income:,.2f}\n"
        f"- Monthly Expenses: ₹{monthly_expenses:,.2f}\n"
        f"- Target Monthly Investment Capacity: ₹{monthly_savings:,.2f}\n"
        f"- Current Liquid Savings: ₹{float(user_data.get('current_savings', 0)):,.2f}\n"
        f"- High-Interest Debts: ₹{float(user_data.get('existing_debts', 0)):,.2f}\n"
        f"- Investment Horizon: {years} years\n"
        f"- Risk Tolerance: {user_data.get('risk_tolerance', user_data.get('risk_level', 'Moderate'))}\n\n"
        f"Calculated Hard Facts (Use these exact numbers):\n"
        f"- Mandatory Emergency Reserve (6 months): ₹{emergency_target['target_amount']:,.2f}\n"
        f"- 10-Year SIP Projection (at {expected_return}% benchmark CAGR):\n"
        f"  * Total Invested: ₹{sip_projections['invested_amount']:,.2f}\n"
        f"  * Projected Returns: ₹{sip_projections['estimated_returns']:,.2f}\n"
        f"  * Expected Total Value: ₹{sip_projections['total_value']:,.2f}\n"
    )

    # 2. Instantiate Agents using native Gemini LLM
    profiler = create_profiler_agent(llm=gemini_llm)
    researcher = create_researcher_agent(llm=gemini_llm)
    strategist = create_strategist_agent(llm=gemini_llm)

    # 3. Define Tasks
    task_profile = Task(
        description=(
            f"Analyze the following user profile and financial context:\n\n{financial_context}\n"
            "Summarize their financial readiness, cash surplus ratio, and define their realistic investment posture."
        ),
        expected_output="A structured assessment of the young investor's current capacity and readiness.",
        agent=profiler
    )

    task_research = Task(
        description=(
            "Use the market tool to inspect broad-market ETFs (e.g., 'VOO' for S&P 500 or 'NIFTYBEES.NS' for Nifty 50). "
            "Use web search if needed to check long-term compounding data for broad-market index funds over 10+ years. "
            "Highlight expense ratios, diversification benefits, and why young investors (18-25) prioritize low-cost indices."
        ),
        expected_output="A concise summary of real-world index fund data, fees, and long-term historical context.",
        agent=researcher
    )

    task_strategy = Task(
        description=(
            "Using the Profiler's readiness assessment and the Researcher's market findings, synthesize a complete, "
            "practical 3-step action plan for this young investor:\n"
            "1. Emergency Fund Plan (using the exact calculated ₹ target).\n"
            "2. Automated Core Index Strategy (mention SIP amount and the 10-year projection figures provided).\n"
            "3. What to Avoid (day trading, crypto hype, futures & options).\n"
            "End with a clear compliance disclaimer stating this is educational analysis, not licensed financial advice."
        ),
        expected_output="A polished, structured educational investment roadmap with exact numbers and clear guidance.",
        agent=strategist
    )

    # 4. Form Crew and Execute
    fingen_crew = Crew(
        agents=[profiler, researcher, strategist],
        tasks=[task_profile, task_research, task_strategy],
        process=Process.sequential,
        verbose=True
    )

    result = fingen_crew.kickoff()
    return str(result.raw if hasattr(result, "raw") else result)
    


# Alias function so app.py can import either run_fingen or run_fingen_pipeline
run_fingen = run_fingen_pipeline


if __name__ == "__main__":
    sample_user = {
        "age": 20,
        "status": "College Student with Part-Time Freelance",
        "monthly_income": 15000,
        "monthly_expenses": 8000,
        "monthly_savings": 3000,
        "time_horizon_years": 10,
        "risk_level": "Moderate (wants long-term growth, low stress)"
    }

    report = run_fingen_pipeline(sample_user)

    print("\n" + "=" * 50)
    print("📋 FINAL FINGEN ROADMAP")
    print("=" * 50 + "\n")
    print(report)