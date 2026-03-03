from flask import Flask, render_template, request, jsonify
import subprocess
import re
import os

app = Flask(__name__)


# ================= HOME PAGE =================
@app.route("/")
def home():
    return render_template("index.html")


# ================= AI SUGGESTED FIX =================
def suggest_fix(error_message):

    error_message = error_message.lower()

    if "syntaxerror" in error_message:
        return "Check missing brackets, quotes, or colons (:)."

    elif "nameerror" in error_message:
        return "You may be using a variable or function before defining it."

    elif "indentationerror" in error_message:
        return "Fix indentation. Python requires proper spacing."

    elif "zerodivisionerror" in error_message:
        return "You are dividing a number by zero."

    elif "typeerror" in error_message:
        return "Check data types used in operations."

    elif "module not found" in error_message:
        return "Install missing module using pip."

    else:
        return "Check logic or syntax near the reported line."


# ================= CODE RUNNER =================
def run_code(code, language):

    try:
        # ---------- PYTHON ----------
        if language == "python":

            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=5
            )

            # If error exists
            if result.stderr:
                match = re.search(r'line (\d+)', result.stderr)

                if match:
                    line = match.group(1)
                    error_text = f"Python Error at line {line}\n\n{result.stderr}"
                else:
                    error_text = result.stderr

                fix = suggest_fix(error_text)

                return {
                    "error": error_text,
                    "fix": fix
                }

            return {
                "output": "No errors found!\n\nOutput:\n" + result.stdout
            }

        return {
            "error": "Unsupported language",
            "fix": "Choose a supported language."
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Execution stopped: Code took too long.",
            "fix": "Avoid infinite loops or input() calls."
        }

    except Exception as e:
        error_message = str(e)
        fix = suggest_fix(error_message)

        return {
            "error": error_message,
            "fix": fix
        }


# ================= DEBUG ROUTE =================
@app.route("/debug", methods=["POST"])
def debug():

    code = request.form.get("code")
    language = request.form.get("language")

    if not code:
        return jsonify({
            "error": "Please enter code.",
            "fix": "Add some code before debugging."
        })

    result = run_code(code, language)

    return jsonify(result)


# ================= RUN SERVER =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)