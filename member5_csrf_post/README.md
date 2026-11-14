# Member 5: CSRF (POST-based Forged Action)

## 1. How to Run & Reproduce

### Prerequisites
- Python 3.8+
- Flask (`pip install flask`)

### Steps:
1. **Start the Web Application:**
   ```bash
   cd member5_csrf_post
   python app.py
   ```
   Application runs on `http://127.0.0.1:5005/`.

2. **Authenticate/Verify User State:**
   - Visit `http://127.0.0.1:5005/` in your browser.
   - Confirm logged in as `alice` with email `alice@university.edu`.

3. **Simulate the Attack:**
   - Open `attacker.html` in a separate browser window.
   - The hidden form submits immediately to `http://127.0.0.1:5005/vuln`.
   - Observe that `alice`'s email is hijacked and updated to `attacker_pwned@malicious.com`.

4. **Verify the Patch:**
   - In `attacker.html`, change `action="http://127.0.0.1:5005/vuln"` to `http://127.0.0.1:5005/patched`.
   - Reload `attacker.html`.
   - The application responds with `HTTP 403 Forbidden: CSRF Token validation failed`, blocking the forgery.

---

## 2. Root Cause Explanation
The vulnerable endpoint (`/vuln`) relies entirely on ambient credentials (cookies) sent automatically by the browser, failing to verify whether the incoming state-changing POST request was intentionally initiated by the legitimate user interface.

---

## 3. Implemented Mitigation
Implemented the **Synchronizer Token Pattern**: A cryptographically random secret token (`session['csrf_token']`) is bound to the user's active session and embedded in legitimate forms as a hidden field. The server strictly rejects incoming POST requests whose submitted token does not match the session token using constant-time comparison (`secrets.compare_digest`).

---

## 4. Alternative Course Mitigations
Beyond synchronizer tokens, modern applications defend against CSRF through:
- **SameSite Cookie Attributes:** Setting `SameSite=Strict` or `SameSite=Lax` on session cookies ensures browsers refuse to attach cookies to cross-site requests.
- **Re-Authentication & Step-Up Auth:** Requiring password re-entry or MFA confirmation before completing critical profile changes.
- **Restricting State-Changing Actions to Non-Idempotent HTTP Methods:** Avoiding GET for state mutations to narrow the attack vector.
