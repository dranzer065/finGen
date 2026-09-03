"""
finGen - Core Financial Calculation Engine
Handles deterministic math for 18-25 wealth planning.
"""

from typing import Dict, Any


def calculate_sip(monthly_investment: float, annual_return_rate: float, years: int) -> Dict[str, Any]:
    """
    Calculate future value of a Systematic Investment Plan (SIP).
    Formula: FV = P * [((1 + i)^n - 1) / i] * (1 + i)
    """
    if monthly_investment <= 0 or years <= 0:
        return {"invested_amount": 0.0, "estimated_returns": 0.0, "total_value": 0.0}

    months = years * 12
    monthly_rate = (annual_return_rate / 100) / 12

    # If return is 0%, simple accumulation
    if monthly_rate == 0:
        invested = monthly_investment * months
        return {
            "invested_amount": round(invested, 2),
            "estimated_returns": 0.0,
            "total_value": round(invested, 2)
        }

    future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    total_invested = monthly_investment * months
    estimated_returns = future_value - total_invested

    return {
        "invested_amount": round(total_invested, 2),
        "estimated_returns": round(estimated_returns, 2),
        "total_value": round(future_value, 2)
    }


def calculate_compound_interest(principal: float, annual_rate: float, years: int, compounding_freq: int = 1) -> Dict[str, Any]:
    """
    Calculate lump sum compound interest.
    Formula: A = P * (1 + r/n)^(n*t)
    """
    if principal <= 0 or years <= 0:
        return {"principal": 0.0, "total_returns": 0.0, "total_value": 0.0}

    rate_decimal = annual_rate / 100
    future_value = principal * ((1 + (rate_decimal / compounding_freq)) ** (compounding_freq * years))
    returns = future_value - principal

    return {
        "principal": round(principal, 2),
        "total_returns": round(returns, 2),
        "total_value": round(future_value, 2)
    }


def calculate_emergency_fund_target(monthly_expenses: float, months_coverage: int = 6) -> Dict[str, Any]:
    """
    Determines emergency reserve size for 18-25 age bracket.
    Default baseline is 6 months of mandatory living costs.
    """
    target = monthly_expenses * months_coverage
    return {
        "monthly_expenses": round(monthly_expenses, 2),
        "months_coverage": months_coverage,
        "target_amount": round(target, 2)
    }