"""
Member 2: OS Command Injection (Direct Shell Concatenation)
Port: 5002
"""
import subprocess
import re
import platform
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Member 2 - Command Injection</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { border: 1px solid #ccc; padding: 20px; border-radius: 8px; margin-bottom: 20px; max-width: 540px; }
        .danger { background-color: #ffe6e6; border-color: #ff9999; }
        .success { background-color: #e6ffe6; border-color: #99ff99; }
        input[type="text"] { width: 95%; padding: 8px; margin: 6px 0; }
        input[type="submit"] { padding: 8px 16px; margin-top: 8px; cursor: pointer; }
        pre { background: #222; color: #0f0; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 13px; }
        code { background-color: #eee; padding: 2px 4px; border-radius: 4px; }
    </style>
</head>
<body>
    <h2>Member 2: OS Command Injection Demo</h2>
    <p>Network Diagnostic Tool (Simulated Ping).</p>
    <p>Payload to test: <code>127.0.0.1 && whoami</code> or <code>127.0.0.1 & whoami</code></p>

    {% if output %}
        <h3>Command Execution Output:</h3>
        <pre>{{ output }}</pre>
    {% endif %}

    <!-- VULNERABLE FORM -->
    <div class="card danger">
        <h3>Vulnerable Diagnostic Tool (/vuln)</h3>
        <p>Passes concatenated strings directly to the system shell (<code>shell=True</code>).</p>
        <form action="{{ url_for('vuln_ping') }}" method="POST">
            <label>IP Address / Hostname:</label><br>
            <input type="text" name="target" placeholder="127.0.0.1 && whoami" required><br>
            <input type="submit" value="Run Diagnostic (Vulnerable Path)">
        </form>
    </div>

    <!-- PATCHED FORM -->
    <div class="card success">
        <h3>Patched Diagnostic Tool (/patched)</h3>
        <p>Enforces strict regex allowlisting and array-based execution without invoking a shell (<code>shell=False</code>).</p>
        <form action="{{ url_for('patched_ping') }}" method="POST">
            <label>IP Address / Hostname:</label><br>
            <input type="text" name="target" placeholder="127.0.0.1" required><br>
            <input type="submit" value="Run Diagnostic (Patched Path)">
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, output=request.args.get("output"))

# --- VULNERABLE CODE PATH ---
@app.route("/vuln", methods=["POST"])
def vuln_ping():
    target = request.form.get("target", "")
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    
    # VULNERABILITY: Raw command string executed in a subshell
    cmd = f"ping {count_flag} 1 {target}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        raw_output = result.stdout + result.stderr
    except Exception as e:
        raw_output = str(e)
        
    return render_template_string(HTML_TEMPLATE, output=raw_output)

# --- PATCHED CODE PATH ---
@app.route("/patched", methods=["POST"])
def patched_ping():
    target = request.form.get("target", "").strip()

    # MITIGATION 1: Strict input allowlisting (valid hostnames/IPv4 only)
    if not re.match(r"^[a-zA-Z0-9.-]+$", target):
        return render_template_string(HTML_TEMPLATE, output="[SECURITY ERROR] Rejected: Target contains disallowed shell metacharacters.")

    count_flag = "-n" if platform.system().lower() == "windows" else "-c"

    # MITIGATION 2: Structured argument list with shell=False (bypasses system shell)
    cmd_args = ["ping", count_flag, "1", target]
    
    try:
        result = subprocess.run(cmd_args, shell=False, capture_output=True, text=True, timeout=5)
        raw_output = result.stdout + result.stderr
    except Exception as e:
        raw_output = str(e)

    return render_template_string(HTML_TEMPLATE, output=raw_output)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
