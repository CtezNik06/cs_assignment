"""
Member 4: CSRF (GET-based Forged Action)
Port: 5004
"""
from flask import Flask, request, session, render_template_string, redirect, url_for, abort
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True
)

ACCOUNT_DATA = {
    "alice": {"status": "Standard", "balance": 1000}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Member 4 - CSRF (GET)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { border: 1px solid #ccc; padding: 20px; border-radius: 8px; margin-bottom: 20px; max-width: 520px; }
        .danger { background-color: #ffe6e6; border-color: #ff9999; }
        .success { background-color: #e6ffe6; border-color: #99ff99; }
        input[type="text"] { width: 90%; padding: 8px; margin: 6px 0; }
        input[type="submit"] { padding: 8px 16px; margin-top: 8px; cursor: pointer; }
        code { background-color: #eee; padding: 2px 4px; border-radius: 4px; }
    </style>
</head>
<body>
    <h2>Member 4: CSRF Demo (GET-based Forged Action)</h2>
    <p>Logged in as: <strong>{{ user }}</strong> | Account Status: <strong style="color: red;">{{ status }}</strong></p>

    {% if message %}
        <p style="color: blue;"><strong>Notification:</strong> {{ message }}</p>
    {% endif %}

    <!-- VULNERABLE SECTION -->
    <div class="card danger">
        <h3>Vulnerable Status Changer (/vuln)</h3>
        <p>Performs state-changing operations via HTTP <code>GET</code> query parameters.</p>
        <a href="{{ url_for('vuln_update_status', status='VIP_MEMBER') }}">Click here to upgrade status to VIP (via GET)</a>
    </div>

    <!-- PATCHED SECTION -->
    <div class="card success">
        <h3>Patched Status Changer (/patched)</h3>
        <p>Restricted strictly to <code>POST</code> requests with an Anti-CSRF Synchronizer Token.</p>
        <form action="{{ url_for('patched_update_status') }}" method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
            <label>New Status:</label><br>
            <input type="text" name="status" value="Verified_User" required><br>
            <input type="submit" value="Update Status (Protected Path)">
        </form>
    </div>
</body>
</html>
"""

@app.before_request
def ensure_session():
    if "user" not in session:
        session["user"] = "alice"
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(24)

@app.route("/")
def index():
    user = session["user"]
    status = ACCOUNT_DATA[user]["status"]
    return render_template_string(
        HTML_TEMPLATE,
        user=user,
        status=status,
        csrf_token=session["csrf_token"],
        message=request.args.get("msg", "")
    )

# --- VULNERABLE CODE PATH ---
@app.route("/vuln", methods=["GET"])
def vuln_update_status():
    user = session.get("user")
    new_status = request.args.get("status", "Standard")
    ACCOUNT_DATA[user]["status"] = new_status
    return redirect(url_for("index", msg=f"[VULN] Account status successfully altered to '{new_status}' via GET!"))

# --- PATCHED CODE PATH ---
@app.route("/patched", methods=["POST"])
def patched_update_status():
    submitted_token = request.form.get("csrf_token")
    expected_token = session.get("csrf_token")

    if not submitted_token or not secrets.compare_digest(submitted_token, expected_token):
        return abort(403, description="Forbidden: CSRF Token validation failed.")

    user = session.get("user")
    new_status = request.form.get("status", "Standard")
    ACCOUNT_DATA[user]["status"] = new_status
    return redirect(url_for("index", msg=f"[PATCHED] Account status securely updated to '{new_status}'."))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5004, debug=True)
