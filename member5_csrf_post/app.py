"""
Member 5: CSRF (POST-based Forged Action)
Port: 5005
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

USERS_DB = {
    "alice": {
        "email": "alice@university.edu"
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Member 5 - CSRF Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .card { border: 1px solid #ccc; padding: 20px; border-radius: 8px; margin-bottom: 20px; max-width: 500px; }
        .danger { background-color: #ffe6e6; border-color: #ff9999; }
        .success { background-color: #e6ffe6; border-color: #99ff99; }
        input[type="email"] { width: 90%; padding: 8px; margin: 8px 0; }
        input[type="submit"] { padding: 8px 16px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Member 5: CSRF Demonstration (POST-based)</h2>
    <p>Logged in as: <strong>{{ user }}</strong> | Current Email: <strong>{{ email }}</strong></p>
    
    {% if message %}
        <p style="color: blue;"><strong>Notification:</strong> {{ message }}</p>
    {% endif %}

    <!-- VULNERABLE FORM -->
    <div class="card danger">
        <h3>Vulnerable Route (/vuln)</h3>
        <p>Accepts state-changing POST requests blindly relying solely on the session cookie.</p>
        <form action="{{ url_for('vuln_update_email') }}" method="POST">
            <label>New Email:</label><br>
            <input type="email" name="email" placeholder="new-email@example.com" required>
            <input type="submit" value="Update Email (Vulnerable)">
        </form>
    </div>

    <!-- PATCHED FORM -->
    <div class="card success">
        <h3>Patched Route (/patched)</h3>
        <p>Enforces a cryptographically secure, per-session Anti-CSRF Synchronizer Token.</p>
        <form action="{{ url_for('patched_update_email') }}" method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
            <label>New Email:</label><br>
            <input type="email" name="email" placeholder="new-email@example.com" required>
            <input type="submit" value="Update Email (Protected)">
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
    email = USERS_DB[user]["email"]
    message = request.args.get("msg", "")
    return render_template_string(
        HTML_TEMPLATE,
        user=user,
        email=email,
        csrf_token=session["csrf_token"],
        message=message
    )

# --- VULNERABLE CODE PATH ---
@app.route("/vuln", methods=["POST"])
def vuln_update_email():
    new_email = request.form.get("email")
    user = session.get("user")
    
    if not user:
        return abort(401, description="Unauthorized")
    
    USERS_DB[user]["email"] = new_email
    return redirect(url_for("index", msg=f"[VULN] Email successfully updated to {new_email}!"))

# --- PATCHED CODE PATH ---
@app.route("/patched", methods=["POST"])
def patched_update_email():
    user = session.get("user")
    if not user:
        return abort(401, description="Unauthorized")

    submitted_token = request.form.get("csrf_token")
    expected_token = session.get("csrf_token")

    if not submitted_token or not secrets.compare_digest(submitted_token, expected_token):
        return abort(403, description="CSRF Token validation failed: Request blocked.")

    new_email = request.form.get("email")
    USERS_DB[user]["email"] = new_email
    return redirect(url_for("index", msg=f"[PATCHED] Email securely updated to {new_email}!"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
