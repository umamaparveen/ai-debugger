from flask import Flask, render_template, request
import subprocess
import re

app = Flask(__name__)


# ---------------- CODE DEBUG FUNCTION ----------------
def run_code(code, language):

    try:
        # ================= PYTHON =================
        if language == "python":

            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True
            )

            if result.stderr:
                line_match = re.search(r'line (\d+)', result.stderr)

                if line_match:
                    line_no = line_match.group(1)
                    return f"""❌ Python Error (Line {line_no})

{result.stderr}

✅ Possible Fix:
Check indentation, missing colon (:), or brackets near line {line_no}.
"""

                return "❌ Python Error:\n" + result.stderr

            return "✅ No errors found!\n\nOutput:\n" + result.stdout


        # ================= JAVA =================
        elif language == "java":

            lines = code.split("\n")

            # check missing semicolon
            for i, line in enumerate(lines, start=1):
                check = line.strip()

                if (
                    check
                    and not check.endswith(";")
                    and "{" not in check
                    and "}" not in check
                    and not check.startswith("//")
                    and "class" not in check
                    and "if" not in check
                    and "for" not in check
                    and "while" not in check
                    and "main" not in check
                ):
                    return f"""❌ Java Syntax Error (Line {i})

Possible missing semicolon ';'
"""

            # class validation
            if "class" not in code:
                return "❌ Java Error: Missing class definition."

            return "✅ No obvious Java syntax errors found."


        # ================= C++ =================
        elif language == "cpp":
            return """⚠ C++ Debugging unavailable.

Server compiler not installed yet.
(Project demo mode)"""


        # ================= UNKNOWN =================
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

    code = request.form.get("code")
    language = request.form.get("language")

    if not code:
        return render_template(
            "index.html",
            result="⚠ Please enter code."
        )

    result = run_code(code, language)

    return render_template(
        "index.html",
        result=result
    )


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)