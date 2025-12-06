from flask import Flask, render_template, request
from main_logic import analyze_stock
import history_cache

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error_message = None

    if request.method == "POST":
        ticker = request.form.get("ticker", "").upper().strip()
        if ticker:
            try:
                result = analyze_stock(ticker)
                history_cache.store_ticker(ticker)
            except Exception as e:
                error_message = f"Error analyzing {ticker}: {str(e)}"
        else:
            error_message = "Please enter a valid ticker."

    history = history_cache.get_history()

    return render_template("index.html",
                           result=result,
                           history=history,
                           error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)
