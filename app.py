from flask import Flask, render_template, request
import subprocess
import requests

app = Flask(__name__)


# ===============================
# RUN CODE & DETECT ERRORS
# ===============================
def run_code(code, language):
    try:

        # ---------- PYTHON ----------
        if language == "python":
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True
            )

            if result.stderr:
                return False, result.stderr
            return True, result.stdout

        # ---------- C++ ----------
        elif language == "cpp":
            return False, "⚠ C++ compiler not installed on server yet."

        # ---------- JAVA ----------
        elif language == "java":
            with open("Main.java", "w") as f:
                f.write(code)

            compile_process = subprocess.run(
                ["javac", "Main.java"],
                capture_output=True,
                text=True
            )

            if compile_process.stderr:
                return False, compile_process.stderr

            run_process = subprocess.run(
                ["java", "Main"],
                capture_output=True,
                text=True
            )

            if run_process.stderr:
                return False, run_process.stderr

            return True, run_process.stdout

        else:
            return False, "Unsupported language"

    except Exception as e:
        return False, str(e)


# ===============================
# FREE AI FIX (HuggingFace API)
# ===============================
def ai_fix_code(code, error):

    prompt = f"""
You are an AI debugging assistant.

Fix the following code and explain briefly.

Code:
{code}

Error:
{error}

Return only corrected code.
"""

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/bigcode/starcoder",
            json={"inputs": prompt},
            timeout=30
        )

        data = response.json()

        if isinstance(data, list):
            return data[0]["generated_text"]

        return "AI suggestion unavailable right now."

    except Exception:
        return "Free AI server busy. Try again later."


# ===============================
# ROUTES
# ===============================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/debug", methods=["POST"])
def debug():

    code = request.form["code"]
    language = request.form["language"]

    success, output = run_code(code, language)

    fixed_code = ""

    if not success:
        fixed_code = ai_fix_code(code, output)

    return render_template(
        "index.html",
        result=output,
        fixed_code=fixed_code,
        language=language,
        code=code
    )


# ===============================
# START SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)