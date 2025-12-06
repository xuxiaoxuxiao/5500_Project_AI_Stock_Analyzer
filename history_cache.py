import json
from pathlib import Path

HISTORY_FILE = Path("history.json")

# Limit: How many items to remember
MAX_HISTORY = 10


def load_cache():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_cache(data):
    HISTORY_FILE.write_text(json.dumps(data, indent=2))


def get_history():
    cache = load_cache()
    return cache.get("history", [])


def store_ticker(ticker):
    cache = load_cache()

    # History list
    history = cache.get("history", [])

    # Add new item at front, remove duplicates
    if ticker in history:
        history.remove(ticker)
    history.insert(0, ticker)

    # Trim to limit
    history = history[:MAX_HISTORY]

    cache["history"] = history
    save_cache(cache)


def get_cached_result(ticker):
    cache = load_cache()
    return cache.get("data", {}).get(ticker)


def store_result(ticker, result):
    cache = load_cache()

    data_cache = cache.get("data", {})
    data_cache[ticker] = result
    cache["data"] = data_cache

    save_cache(cache)
