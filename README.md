# finGen 🚀
### Autonomous Multi-Agent Financial Literacy & Wealth-Building Engine (Ages 18–25)

finGen is an autonomous, multi-agent AI system engineered to guide young adults (ages 18–25) toward long-term financial independence. Built with **CrewAI**, **Google Gemini**, and **Tavily Search**, finGen analyzes cash flows, fetches live ETF and macroeconomic benchmark data, computes deterministic compound projections, and generates tailored wealth roadmaps.

---

## 🏛️ System Architecture

The pipeline executes sequentially through specialized autonomous agents:

```text
User Financial Profile
        │
        ▼
┌───────────────────────────┐
│   Youth Profiler Agent    │ ➔ Computes surplus ratio, buffer, and liquidity needs
└─────────────┬─────────────┘
        │
        ▼
┌───────────────────────────┐
│ Market Researcher Agent   │ ➔ Inspects live ETF benchmarks (yfinance & Tavily)
└─────────────┬─────────────┘
        │
        ▼
┌───────────────────────────┐
│ Educational Strategist    │ ➔ Integrates deterministic SIP math & guardrails
└─────────────┬─────────────┘
        │
        ▼
Actionable Educational Roadmap