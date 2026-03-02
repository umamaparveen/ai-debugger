from flask import Flask, render_template, request
import subprocess
import re

app = Flask(__name__)


# ---------------- CODE RUNNER ----------------
def run_code(code, language):

    try:
        # ---------------- PYTHON ----------------
        if language == "python":

            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True
            )

            if result.stderr:
                import re
                line_match = re.search(r'line (\d+)', result.stderr)

                if line_match:
                    line_no = line_match.group(1)
                    return f"❌ Python Error at line {line_no}\n\n{result.stderr}"

                return "❌ Error:\n" + result.stderr

            return "✅ No errors found!\n\nOutput:\n" + result.stdout


        # ---------------- JAVA (SMART CHECK) ----------------
        elif language == "java":

            lines = code.split("\n")

            # missing semicolon check
            for i, line in enumerate(lines, start=1):
                line = line.strip()

                if (
                    line
                    and not line.endswith(";")
                    and "{" not in line
                    and "}" not in line
                    and "class" not in line
                    and "if" not in line
                    and "for" not in line
                    and "while" not in line
                ):
                    return f"❌ Java Syntax Error near line {i}\nPossible missing semicolon ';'"

            # class check
            if "class" not in code:
                return "❌ Java Error: Missing class definition."

            return "✅ No obvious Java syntax errors found."


        # ---------------- C++ ----------------
        elif language == "cpp":
            return "⚠ C++ debugging unavailable (compiler not installed on server)."


        else:
            return "Unsupported language."

    except Exception as e:
        return "Server Error:\n" + str(e)
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