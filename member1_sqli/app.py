"""
Member 1: SQL Injection (In-Band Authentication Bypass)
Port: 5001
"""
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    with conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT);")
        conn.execute("DELETE FROM users;")
        conn.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'Sup3rS3cur3P@ssw0rd!', 'Administrator');")
        conn.execute("INSERT INTO users (username, password, role) VALUES ('alice', 'alice123', 'Standard User');")
    conn.close()

init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Member 1 - SQL Injection</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { border: 1px solid #ccc; padding: 20px; border-radius: 8px; margin-bottom: 20px; max-width: 520px; }
        .danger { background-color: #ffe6e6; border-color: #ff9999; }
        .success { background-color: #e6ffe6; border-color: #99ff99; }
        input[type="text"], input[type="password"] { width: 95%; padding: 8px; margin: 6px 0; }
        input[type="submit"] { padding: 8px 16px; margin-top: 8px; cursor: pointer; }
        code { background-color: #eee; padding: 2px 4px; border-radius: 4px; }
    </style>
</head>
<body>
    <h2>Member 1: SQL Injection Demo (Auth Bypass)</h2>
    <p>Target account: <code>admin</code> (Password is hidden).</p>
    <p>Payload to test: <code>admin' --</code> or <code>' OR 1=1 --</code></p>

    {% if message %}
        <div style="padding: 10px; margin-bottom: 15px; background: #eef; border: 1px solid #99f;">
            <strong>Result:</strong> {{ message }}
        </div>
    {% endif %}

    <!-- VULNERABLE FORM -->
    <div class="card danger">
        <h3>Vulnerable Login (/vuln)</h3>
        <p>Uses raw string formatting to concatenate user input into the SQL statement.</p>
        <form action="{{ url_for('vuln_login') }}" method="POST">
            <label>Username:</label><br>
            <input type="text" name="username" placeholder="e.g. admin' --" required><br>
            <label>Password:</label><br>
            <input type="password" name="password" placeholder="Any password"><br>
            <input type="submit" value="Login (Vulnerable Path)">
        </form>
    </div>

    <!-- PATCHED FORM -->
    <div class="card success">
        <h3>Patched Login (/patched)</h3>
        <p>Uses parameterized queries (prepared statement placeholders).</p>
        <form action="{{ url_for('patched_login') }}" method="POST">
            <label>Username:</label><br>
            <input type="text" name="username" placeholder="e.g. admin' --" required><br>
            <label>Password:</label><br>
            <input type="password" name="password" placeholder="Password"><br>
            <input type="submit" value="Login (Patched Path)">
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    msg = request.args.get("msg", "")
    return render_template_string(HTML_TEMPLATE, message=msg)

# --- VULNERABLE CODE PATH ---
@app.route("/vuln", methods=["POST"])
def vuln_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # VULNERABILITY: Direct SQL string interpolation
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect(url_for("index", msg=f"[AUTH BYPASSED] Successfully logged in as '{user['username']}' with role '{user['role']}'! (Query executed: {query})"))
        else:
            return redirect(url_for("index", msg="[AUTH FAILED] Invalid credentials."))
    except sqlite3.OperationalError as e:
        conn.close()
        return redirect(url_for("index", msg=f"[SQL ERROR] {str(e)}"))

# --- PATCHED CODE PATH ---
@app.route("/patched", methods=["POST"])
def patched_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # MITIGATION: Parameterized query ensures input is treated strictly as data, not code
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return redirect(url_for("index", msg=f"[SECURE AUTH] Successfully logged in as '{user['username']}' with role '{user['role']}'."))
    else:
        return redirect(url_for("index", msg="[PATCHED] Access Denied: Invalid credentials. Exploit safely neutralized!"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
