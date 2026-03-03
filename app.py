from flask import Flask, render_template, request, jsonify
import subprocess
import re
import os

app = Flask(__name__)


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- FIX SUGGESTION ----------------
def suggest_fix(error):
    error = error.lower()

    if "syntaxerror" in error:
        return "Check missing brackets, quotes, or colons."

    if "nameerror" in error:
        return "A variable or function name is not defined. Check spelling."

    if "indentationerror" in error:
        return "Fix indentation spacing. Python requires consistent indentation."

    if "typeerror" in error:
        return "You used incompatible data types together."

    return "Check your code logic and syntax."


# ---------------- EXPLANATION FEATURE ⭐ ----------------
def explain_error(error):
    error = error.lower()

    if "syntaxerror" in error:
        return "Python could not understand your code structure. This usually happens when symbols like quotes, brackets, or colons are missing."

    if "nameerror" in error:
        return "You are trying to use something that Python does not recognize as defined."

    if "indentationerror" in error:
        return "Python uses indentation to understand blocks of code. Incorrect spacing caused this error."

    if "typeerror" in error:
        return "You combined two values of different types that cannot work together."

    return "An error occurred while executing the program. Review the message to locate the issue."


# ---------------- RUN CODE ----------------
def run_code(code, language):

    if language != "python":
        return {
            "error": "Unsupported language",
            "fix": "Choose a supported language.",
            "explanation": "Currently only Python debugging is enabled."
        }

    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.stderr:
            error_message = result.stderr
            fix = suggest_fix(error_message)
            explanation = explain_error(error_message)

            return {
                "error": error_message,
                "fix": fix,
                "explanation": explanation
            }

        return {
            "output": result.stdout
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Execution timeout",
            "fix": "Avoid infinite loops or input statements.",
            "explanation": "Your program ran too long without finishing."
        }


# ---------------- DEBUG ROUTE ----------------
@app.route("/debug", methods=["POST"])
def debug():

    code = request.form.get("code")
    language = request.form.get("language")

    result = run_code(code, language)

    return jsonify(result)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)