from dataclasses import dataclass
import numpy as np
import yfinance as yf


@dataclass
class StockIndicators:
    ticker: str
    last_price: float
    sma_20: float
    sma_50: float
    rsi_14: float


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
        return 100.0

    rs = avg_gain / avg_loss
    return float(100 - (100 / (1 + rs)))


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
    rsi_14 = compute_rsi(close_prices.values)
    last_price = float(close_prices.iloc[-1])

    return StockIndicators(
        ticker=ticker.upper(),
        last_price=last_price,
        sma_20=sma_20,
        sma_50=sma_50,
        rsi_14=rsi_14,
    )



