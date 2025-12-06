
from dataclasses import dataclass
from typing import Dict, Any

import yfinance as yf
import numpy as np


from openai import OpenAI

# =========================
# Config & Setup
# =========================


from dotenv import load_dotenv
from pathlib import Path
import os

# Explicitly point to .env next to this file
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        f"OPENAI_API_KEY not found. Expected it in {dotenv_path}. "
        "Make sure .env exists and contains OPENAI_API_KEY=..."
    )



if not OPENAI_API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment or .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)


@dataclass
class StockIndicators:
    ticker: str
    last_price: float
    sma_20: float
    sma_50: float
    rsi_14: float


# =========================
# Indicator Calculation
# =========================

def compute_rsi(prices, period: int = 14) -> float:
    """
    Compute RSI (Relative Strength Index) for a given price series.
    prices: list/array of closing prices (most recent last).
    """
    if len(prices) < period + 1:
        return float("nan")

    prices = np.array(prices, dtype=float)
    deltas = np.diff(prices)

    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)

    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])

    if avg_loss == 0:
        return 100.0  # no losses => max RSI

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)


def get_stock_indicators(ticker: str) -> StockIndicators:
    """
    Fetch historical data with yfinance and compute basic indicators.
    """
    data = yf.download(ticker, period="6mo", interval="1d", progress=False)

    if data.empty:
        raise ValueError(f"No data returned for ticker {ticker}")

    close_prices = data["Close"]

    if len(close_prices) < 50:
        raise ValueError(f"Not enough data for {ticker} to compute 50-day SMA.")

    sma_20 = float(close_prices.tail(20).mean())
    sma_50 = float(close_prices.tail(50).mean())
    rsi_14 = compute_rsi(close_prices.values, period=14)
    last_price = float(close_prices.iloc[-1])

    return StockIndicators(
        ticker=ticker.upper(),
        last_price=last_price,
        sma_20=sma_20,
        sma_50=sma_50,
        rsi_14=rsi_14,
    )


# =========================
# ChatGPT Analysis
# =========================

def ask_chatgpt_for_recommendation(indicators: StockIndicators) -> Dict[str, Any]:
    """
    Send the indicators to ChatGPT and ask for a Buy/Hold/Sell suggestion.
    """
    system_prompt = """\
You are an assistant that does basic, educational stock analysis.
You are NOT a financial advisor and must always remind the user that your output is not financial advice.
Use only the data provided. Do NOT invent real-time data.
Make a simple recommendation: Buy, Hold, or Sell, and explain reasoning in plain English.
"""

    user_prompt = f"""
Please analyze the following stock based on simple technical indicators.

Ticker: {indicators.ticker}
Last Close Price: {indicators.last_price:.2f}

Indicators:
- 20-day Simple Moving Average (SMA20): {indicators.sma_20:.2f}
- 50-day Simple Moving Average (SMA50): {indicators.sma_50:.2f}
- 14-day RSI: {indicators.rsi_14:.2f}

Rules of thumb you can use (but you may override if justified):
- If price > SMA20 > SMA50 and RSI between 40 and 70 -> mild bullish bias.
- If price < SMA20 < SMA50 and RSI between 30 and 60 -> mild bearish bias.
- RSI > 70 -> possibly overbought.
- RSI < 30 -> possibly oversold.

Return a short JSON object with keys:
- "action": one of ["BUY", "HOLD", "SELL"]
- "confidence": integer 1–10
- "explanation": short paragraph (3–6 sentences) in plain English
- "disclaimer": brief disclaimer that this is NOT financial advice.

DO NOT include any backticks or code fences, just raw JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    # The model returns JSON as text; parse it safely.
    import json
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        # fallback: wrap as explanation-only
        parsed = {
            "action": "HOLD",
            "confidence": 5,
            "explanation": content,
            "disclaimer": "This is not financial advice.",
        }

    return parsed


# =========================
# Main CLI
# =========================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Basic stock analysis with ChatGPT.")
    parser.add_argument("ticker", type=str, help="Stock ticker symbol, e.g. AAPL, TSLA")
    args = parser.parse_args()

    ticker = args.ticker.upper()
    print(f"Fetching data for {ticker}...")

    try:
        indicators = get_stock_indicators(ticker)
    except Exception as e:
        print(f"Error while fetching data or computing indicators: {e}")
        return

    print("\n=== Indicators ===")
    print(f"Ticker       : {indicators.ticker}")
    print(f"Last Price   : {indicators.last_price:.2f}")
    print(f"SMA20        : {indicators.sma_20:.2f}")
    print(f"SMA50        : {indicators.sma_50:.2f}")
    print(f"RSI(14)      : {indicators.rsi_14:.2f}")

    print("\nAsking ChatGPT for a basic recommendation...")
    rec = ask_chatgpt_for_recommendation(indicators)

    print("\n=== ChatGPT Recommendation (Educational Only) ===")
    print(f"Action      : {rec.get('action', 'N/A')}")
    print(f"Confidence  : {rec.get('confidence', 'N/A')}/10")
    print(f"Explanation : {rec.get('explanation', '')}")
    print(f"Disclaimer  : {rec.get('disclaimer', '')}")


if __name__ == "__main__":
    main()
