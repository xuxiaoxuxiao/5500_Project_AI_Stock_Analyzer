📈 AI Stock Analyzer

AI Stock Analyzer is a modern, lightweight stock analysis web application that combines:

✔ Real market data from Yahoo Finance
✔ Basic technical indicators (SMA20, SMA50, RSI)
✔ AI-driven Buy/Hold/Sell recommendations powered by ChatGPT
✔ Search history caching to improve speed and reduce API cost
✔ Clean and professional web UI using Flask

⚠️ This app is for educational purposes only — not financial advice.

🚀 Features
Feature	Description
🔍 Search any stock ticker	e.g., AAPL, TSLA, MSFT
📊 Technical indicators	SMA20, SMA50, RSI
🤖 AI recommendation	Buy / Hold / Sell + explanation
📡 Real-time data	Pulled via Yahoo Finance
💾 Smart caching	Saves API tokens + much faster after first use
🧠 Search history	Quick access to previously analyzed tickers
🎨 Modern UI	Clean design, responsive layout
🧱 Tech Stack
Category	Technology
Backend	Python, Flask
Data Source	Yahoo Finance (yfinance)
AI Model	OpenAI GPT (gpt-4o-mini)
Frontend	HTML, CSS, JavaScript
Caching	JSON-based local store

📦 Project Structure
📁 project_root/
│
├── app.py                  # Flask web server
├── main_logic.py           # Fetch indicators + AI analysis
├── indicators.py           # RSI / SMA calculations
├── chatgpt_agent.py        # OpenAI recommendation request
├── history_cache.py        # Cache + search history
│
├── templates/
│   └── index.html          # Web interface
│
└── static/
    ├── style.css           # Modern UI styling
    └── script.js           # Client-side UX interactions
