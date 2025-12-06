# 📈 AI Stock Analyzer

AI Stock Analyzer is a lightweight web application that analyzes U.S. stock performance using:

- Real market data from Yahoo Finance
- Technical indicators (SMA20, SMA50, RSI)
- AI-generated Buy/Hold/Sell recommendations powered by ChatGPT
- A clean modern UI with search history support

⚠️ This tool is for **educational purposes only** and not financial advice.

---

## 🚀 Features

- Search any U.S. stock ticker (e.g., AAPL, TSLA, NVDA)
- Calculates SMA20, SMA50, and RSI indicators
- Generates a simple actionable recommendation via OpenAI API
- Remembers recent ticker searches for quick access
- Modern centered UI design (mobile friendly)
- Caches results locally to reduce API cost and increase speed

---

## 🧰 Technology Stack

| Area | Tech |
|------|-----|
| Backend | Python 3, Flask |
| Data Source | `yfinance` - Yahoo Finance |
| AI Model | OpenAI GPT (`gpt-4o-mini`) |
| Frontend | HTML + CSS (custom modern design) |
| Caching | Local JSON history |

## 📘 How to Use AI Stock Analyzer

Follow these simple steps to analyze any U.S. stock:

---

### 1️⃣ Start the Application

Run this command inside the project folder:

```bash
python app.py

Then open your browser and visit:

👉 http://127.0.0.1:5000/

2️⃣ Enter a Stock Ticker Symbol

Type a valid stock code into the search box, for example:

AAPL
TSLA
NVDA
META
AMZN


Then click Analyze.