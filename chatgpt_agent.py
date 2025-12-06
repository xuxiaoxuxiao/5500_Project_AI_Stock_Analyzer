import json
from openai import OpenAI

from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing in .env")

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_chatgpt_for_recommendation(indicators):
    """
    Send stock indicators to ChatGPT and return a recommendation dict.
    """
    system_prompt = """\
You are an assistant that does basic, educational stock analysis.
You are NOT a financial advisor and must always remind the user that your output is not financial advice.
Use only the data provided. Do NOT invent real-time data.
Return a Buy/Hold/Sell suggestion with an explanation.
"""

    user_prompt = f"""
Please analyze the following stock based on simple technical indicators.

Ticker: {indicators.ticker}
Last Close Price: {indicators.last_price:.2f}

Indicators:
- 20-day SMA: {indicators.sma_20:.2f}
- 50-day SMA: {indicators.sma_50:.2f}
- 14-day RSI: {indicators.rsi_14:.2f}

Return a JSON object with:
- "action"
- "confidence" (1–10)
- "explanation"
- "disclaimer"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    # Try to parse the result as JSON
    try:
        content_clean = content.strip().strip("`")
        content_clean = content_clean.replace("json", "").replace("```", "").strip()
        return json.loads(content_clean)
    except json.JSONDecodeError:
        return {
            "action": "HOLD",
            "confidence": 5,
            "explanation": content,
            "disclaimer": "This is not financial advice.",
        }
