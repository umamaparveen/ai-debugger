from flask import Flask, render_template, request
import subprocess
import re

app = Flask(__name__)


# ---------------- CODE RUNNER ----------------
def run_code(code, language):

    try:
        # ---------- PYTHON ----------
        if language == "python":

            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True
            )

            # If error exists
            if result.stderr:

                # Try extracting line number
                line_match = re.search(r'line (\d+)', result.stderr)

                if line_match:
                    line_no = line_match.group(1)
                    return f"""❌ Error Found (Line {line_no})

{result.stderr}

✅ Possible Fix:
Check syntax near line {line_no}.
Missing colon, bracket, or indentation issue possible.
"""

                return "❌ Error:\n" + result.stderr

            # No error
            return "✅ No errors found!\n\nOutput:\n" + result.stdout


        # ---------- JAVA (Demo Syntax Check) ----------
        elif language == "java":
            if "class" not in code:
                return "❌ Java Error: Missing class definition."
            return "✅ Java syntax looks correct."


        # ---------- C++ ----------
        elif language == "cpp":
            return "⚠ C++ compiler not installed on server yet."


        # ---------- UNKNOWN ----------
        else:
            return "Unsupported language selected."

    except Exception as e:
        return "Server Error:\n" + str(e)


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/debug", methods=["POST"])
def debug():

    code = request.form.get("code", "")
    language = request.form.get("language", "")

    if not code:
        return render_template(
            "index.html",
            result="⚠ Please enter code before debugging."
        )

    result = run_code(code, language)

    # IMPORTANT: ALWAYS RETURN
    return render_template("index.html", result=result)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)