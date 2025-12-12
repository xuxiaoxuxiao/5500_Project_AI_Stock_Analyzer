from flask import Flask, render_template, request, session
from main_logic import analyze_stock

app = Flask(__name__)
app.secret_key = "supersecret123"   # needed for session


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error_message = None

    # Initialize session history
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        ticker = request.form.get("ticker", "").upper().strip()

        if ticker:
            try:
                # Run the stock analysis
                result = analyze_stock(ticker)

                # Store it in session history
                if ticker not in session["history"]:
                    session["history"].append(ticker)
                    session.modified = True

            except Exception as e:
                error_message = f"Error analyzing {ticker}: {str(e)}"
        else:
            error_message = "Please enter a valid ticker."

    return render_template(
        "index.html",
        result=result,
        history=session["history"],
        error_message=error_message
    )


@app.post("/clear_history")
def clear_history():
    session["history"] = []
    session.modified = True
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)
