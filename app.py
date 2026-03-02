from flask import Flask, render_template, request
import subprocess
import re

app = Flask(__name__)


# ---------------- DEBUG FUNCTION ----------------
def run_code(code, language):

    print("LANGUAGE RECEIVED:", language)  # debug check

    try:
        # ========= PYTHON =========
        if language == "python":

            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True
            )

            if result.stderr:
                match = re.search(r'line (\d+)', result.stderr)
                if match:
                    line = match.group(1)
                    return f"❌ Python Error at line {line}\n\n{result.stderr}"

                return "❌ Python Error:\n" + result.stderr

            return "✅ No errors found!\n\nOutput:\n" + result.stdout


        # ========= JAVA =========
        elif language == "java":

            lines = code.split("\n")

            for i, line in enumerate(lines, start=1):
                l = line.strip()

                if (
                    l
                    and not l.endswith(";")
                    and "{" not in l
                    and "}" not in l
                    and not l.startswith("//")
                    and "class" not in l
                    and "if" not in l
                    and "for" not in l
                    and "while" not in l
                    and "main" not in l
                ):
                    return f"❌ Java Syntax Error at line {i}\nMissing semicolon ';'"

            if "class" not in code:
                return "❌ Java Error: Missing class definition."

            return "✅ Java checked successfully (No obvious syntax errors)."


        # ========= C++ =========
        elif language == "cpp":
            return "⚠ C++ compiler not installed on server yet."


        else:
            return f"Unknown language received: {language}"

    except Exception as e:
        return str(e)


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/debug", methods=["POST"])
def debug():

    code = request.form.get("code")
    language = request.form.get("language")

    result = run_code(code, language)

    return render_template("index.html", result=result)


# ---------------- RUN ----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)