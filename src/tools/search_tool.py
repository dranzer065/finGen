"""
finGen - Web Search Tool
Fetches structured financial news and macro trends using Tavily Search API.
"""

import os
from dotenv import load_dotenv
from tavily import TavilyClient
from crewai.tools import tool

# Load API keys from .env
load_dotenv()


def search_financial_web(query: str, max_results: int = 4) -> str:
    """Core logic to search the web using Tavily with finance context."""
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return (
            "Error: TAVILY_API_KEY is missing from environment variables. "
            "Please add it to your .env file."
        )

    try:
        client = TavilyClient(api_key=api_key)
        # Contextually bias search toward education and verified macro analysis
        search_query = f"{query} long term investing index funds 18-25 years"
        
        response = client.search(
            query=search_query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=True
        )

        results = []
        if response.get("answer"):
            results.append(f"Direct Overview: {response['answer']}\n")

        for item in response.get("results", []):
            results.append(
                f"- Title: {item.get('title')}\n"
                f"  Snippet: {item.get('content')}\n"
                f"  Source: {item.get('url')}\n"
            )

        return "\n".join(results) if results else "No relevant financial data found."

    except Exception as e:
        return f"Error executing web search: {str(e)}"


@tool("web_search")
def search_tool(query: str) -> str:
    """
    Searches the live internet for macroeconomic indicators, central bank policies,
    inflation trends, and low-cost index investing data for young adults.
    """
    return search_financial_web(query)


if __name__ == "__main__":
    # Quick standalone test
    print("Testing Tavily Search Tool...")
    sample_query = "Nifty 50 vs S&P 500 returns last 10 years"
    print(search_financial_web(sample_query, max_results=2))