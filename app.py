from flask import Flask, render_template, request
import os
import subprocess
import re

app = Flask(__name__)


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- RUN CODE ----------------
def run_code(code, language):

    # ================= PYTHON =================
    if language == "python":
        try:
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.stderr:
                match = re.search(r'line (\d+)', result.stderr)
                if match:
                    line = match.group(1)
                    return f"❌ Python Error at line {line}\n\n{result.stderr}"

                return "❌ Python Error:\n" + result.stderr

            return "✅ No errors found!\n\nOutput:\n" + result.stdout

        except subprocess.TimeoutExpired:
            return "⏱ Execution stopped: Code took too long."

    return "⚠ Unsupported language."


# ---------------- DEBUG ROUTE ----------------
@app.route("/debug", methods=["POST"])
def debug():
    try:
        code = request.form.get("code")
        language = request.form.get("language")

        if not code:
            return render_template("index.html", result="⚠ Please enter code.")

        result = run_code(code, language)

        return render_template("index.html", result=result)

    except Exception as e:
        return render_template("index.html", result=f"Error: {str(e)}")


# ---------------- START APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)