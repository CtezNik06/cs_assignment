"""
Member 3: Stored Cross-Site Scripting (XSS)
Port: 5003
"""
from flask import Flask, request, render_template_string, redirect, url_for
import html

app = Flask(__name__)

VULN_COMMENTS = []
PATCHED_COMMENTS = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Member 3 - Stored XSS</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { border: 1px solid #ccc; padding: 20px; border-radius: 8px; margin-bottom: 20px; max-width: 540px; }
        .danger { background-color: #ffe6e6; border-color: #ff9999; }
        .success { background-color: #e6ffe6; border-color: #99ff99; }
        textarea { width: 95%; height: 60px; padding: 8px; margin: 6px 0; }
        input[type="submit"] { padding: 8px 16px; margin-top: 8px; cursor: pointer; }
        .comment-box { background: white; border: 1px solid #ddd; padding: 8px; margin: 6px 0; border-radius: 4px; }
        code { background-color: #eee; padding: 2px 4px; border-radius: 4px; }
    </style>
</head>
<body>
    <h2>Member 3: Stored XSS Demo (Community Guestbook)</h2>
    <p>Payload to test: <code>&lt;script&gt;alert('XSS-Cookie:' + document.cookie)&lt;/script&gt;</code> or <code>&lt;img src=x onerror=alert('Stored-XSS')&gt;</code></p>

    <!-- VULNERABLE SECTION -->
    <div class="card danger">
        <h3>Vulnerable Guestbook (/vuln)</h3>
        <p>Renders stored user input with <code>|safe</code>, bypassing automatic HTML escaping.</p>
        <form action="{{ url_for('vuln_comment') }}" method="POST">
            <textarea name="comment" placeholder="Leave a comment..." required></textarea><br>
            <input type="submit" value="Post Comment (Vulnerable Path)">
        </form>
        <h4>Comments Log:</h4>
        {% for c in vuln_comments %}
            <div class="comment-box">
                <!-- VULNERABILITY: Raw HTML rendered into DOM -->
                {{ c | safe }}
            </div>
        {% else %}
            <p><em>No comments yet.</em></p>
        {% endfor %}
    </div>

    <!-- PATCHED SECTION -->
    <div class="card success">
        <h3>Patched Guestbook (/patched)</h3>
        <p>Applies context-aware HTML entity encoding on all stored user content.</p>
        <form action="{{ url_for('patched_comment') }}" method="POST">
            <textarea name="comment" placeholder="Leave a comment..." required></textarea><br>
            <input type="submit" value="Post Comment (Patched Path)">
        </form>
        <h4>Comments Log:</h4>
        {% for c in patched_comments %}
            <div class="comment-box">
                <!-- MITIGATION: Standard template escaping converts < > & " into HTML entities -->
                {{ c }}
            </div>
        {% else %}
            <p><em>No comments yet.</em></p>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, vuln_comments=VULN_COMMENTS, patched_comments=PATCHED_COMMENTS)

# --- VULNERABLE CODE PATH ---
@app.route("/vuln", methods=["POST"])
def vuln_comment():
    comment = request.form.get("comment", "")
    VULN_COMMENTS.append(comment)
    return redirect(url_for("index"))

# --- PATCHED CODE PATH ---
@app.route("/patched", methods=["POST"])
def patched_comment():
    comment = request.form.get("comment", "")
    safe_comment = html.escape(comment)
    PATCHED_COMMENTS.append(safe_comment)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=True)
