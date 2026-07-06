import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_market_impact(ticker, title, publisher, sentiment, score):
    prompt = f"""
You are a financial news analyst.

Analyze this news headline for market impact.

Ticker: {ticker}
Publisher: {publisher}
Headline: {title}
FinBERT Sentiment: {sentiment}
FinBERT Score: {score}

Return ONLY valid JSON with this structure:
{{
  "reasoning": "...",
  "impact_level": "Low | Medium | High",
  "time_horizon": "Short-Term | Medium-Term | Long-Term",
  "category": "Earnings | Product | Legal/Regulatory | Macro | Leadership | AI/Technology | Competition | Manufacturing | Other",
  "confidence": 0.0
}}

Rules:
- Be realistic.
- Do not give financial advice.
- Explain why the headline may matter to investors.
- If the headline is not directly relevant to the ticker, say that in the reasoning.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You analyze financial news headlines and return structured JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return {
            "reasoning": f"AI analysis unavailable: {str(e)}",
            "impact_level": "Unknown",
            "time_horizon": "Unknown",
            "category": "Other",
            "confidence": 0.0
        }