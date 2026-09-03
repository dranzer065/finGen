"""
finGen - Market Data Tool
Pulls verifiable index and ETF metrics using Yahoo Finance (yfinance).
"""

import json
import yfinance as yf
from crewai.tools import tool


def get_market_data(ticker_symbol: str) -> str:
    """Core logic to fetch fundamental data for an ETF or Index fund."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        # Extract essential metrics for 18-25 long-term indexing
        data = {
            "symbol": ticker_symbol.upper(),
            "name": info.get("shortName") or info.get("longName", "N/A"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice", "N/A"),
            "currency": info.get("currency", "USD"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "expense_ratio": info.get("annualReportExpenseRatio") or info.get("netExpenseRatio", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "category": info.get("category", "Index Fund / ETF"),
            "summary": info.get("longBusinessSummary", "No summary available.")[:300] + "..."
        }

        return json.dumps(data, indent=2)

    except Exception as e:
        return f"Error fetching market data for '{ticker_symbol}': {str(e)}"


@tool("fetch_market_benchmark")
def market_tool(ticker_symbol: str) -> str:
    """
    Fetches real-time price, 52-week range, expense ratio, and fundamentals
    for a given ETF or stock index symbol (e.g., 'VOO', 'SPY', 'NIFTYBEES.NS').
    """
    return get_market_data(ticker_symbol)


if __name__ == "__main__":
    # Quick standalone test
    print("Testing Market Tool with S&P 500 ETF (VOO)...")
    result = get_market_data("VOO")
    print(result)