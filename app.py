from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/debug", methods=["POST"])
def debug():
    code = request.form.get("code")
    language = request.form.get("language")

    if not code:
        return render_template("index.html", result="⚠ Please enter code.")

    result = run_code(code, language)   # your existing function

    return render_template("index.html", result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)