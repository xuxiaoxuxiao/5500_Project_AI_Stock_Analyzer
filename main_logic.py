import history_cache
from indicators import get_stock_indicators
from chatgpt_agent import ask_chatgpt_for_recommendation
import numpy as np


def analyze_stock(ticker: str):
    # Try cached first
    cached = history_cache.get_cached_result(ticker)
    if cached:
        print(f"⚡ Using cached data for {ticker}")
        return cached

    print(f"📡 Fetching fresh data for {ticker}")
    indicators = get_stock_indicators(ticker)
    recommendation = ask_chatgpt_for_recommendation(indicators)

    rsi_value = indicators.rsi_14
    if not rsi_value or np.isnan(rsi_value):
        rsi_value = "N/A"
    else:
        rsi_value = f"{rsi_value:.2f}"

    result = {
        "ticker": indicators.ticker,
        "last_price": f"{indicators.last_price:.2f}",
        "sma20": f"{indicators.sma_20:.2f}",
        "sma50": f"{indicators.sma_50:.2f}",
        "rsi": rsi_value,
        "recommendation": recommendation,
        "chart_data": []  # filled soon
    }

    history_cache.store_result(ticker, result)
    return result
