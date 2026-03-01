from flask import Flask, render_template, request
import subprocess
import tempfile
import re

app = Flask(__name__)


# ---------- DEBUG ENGINE ----------
def analyze_code(code):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
        f.write(code)
        filename = f.name

    try:
        result = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return {
                "status": "success",
                "message": "✅ Code executed successfully. No errors found."
            }

        error_output = result.stderr

        # Extract line number
        line_match = re.search(r'line (\d+)', error_output)
        line_number = line_match.group(1) if line_match else "Unknown"

        # Detect error type
        if "SyntaxError" in error_output:
            fix = "Check missing brackets, quotes, or colons."
            error_type = "SyntaxError"

        elif "NameError" in error_output:
            fix = "Variable or function not defined. Check spelling or declaration."
            error_type = "NameError"

        elif "IndentationError" in error_output:
            fix = "Fix indentation spacing (tabs or spaces mismatch)."
            error_type = "IndentationError"

        else:
            fix = "Review logic or variable usage."
            error_type = "Runtime Error"

        return {
            "status": "error",
            "error_type": error_type,
            "line": line_number,
            "details": error_output.splitlines()[-1],
            "fix": fix
        }

    except Exception as e:
        return {
            "status": "error",
            "error_type": "System Error",
            "line": "-",
            "details": str(e),
            "fix": "Try running code again."
        }


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/debug", methods=["GET", "POST"])
def debug():
    if request.method == "GET":
        return redirect("/")
def debug():
    code = request.form["code"]
    result = analyze_code(code)
    return render_template("index.html", result=result, code=code)


if __name__ == "__main__":
    app.run(debug=True)