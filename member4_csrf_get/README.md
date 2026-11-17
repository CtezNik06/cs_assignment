# Member 4: Aayushi Bansal - CSRF (GET-based Forged Action)

## 1. How to Run & Reproduce

### Prerequisites
- Python 3.8+
- Flask (`pip install flask`)

### Steps:
1. **Start the Application Server:**
   ```bash
   cd member4_csrf_get
   python app.py
   ```
   Application runs on `http://127.0.0.1:5004/`.

2. **Authenticate Victim:**
   - Open `http://127.0.0.1:5004/` in your browser.
   - Confirm logged in as `alice` with initial status `Standard`.

3. **Trigger the Exploit:**
   - Open `attacker.html` in another browser tab (or serve via `python -m http.server 8084`).
   - The browser attempts to load the `<img src="http://127.0.0.1:5004/vuln?status=ACCOUNT_HIJACKED_BY_CSRF">` element.
   - Switch back to `http://127.0.0.1:5004/` and refresh: `alice`'s account status has changed to `ACCOUNT_HIJACKED_BY_CSRF` without her consent.

4. **Verify the Patch:**
   - The `/patched` route strictly enforces HTTP `POST` alongside a unique Synchronizer Token.
   - Attempting to invoke the patched route via GET (`http://127.0.0.1:5004/patched?status=TEST`) results in `405 Method Not Allowed`.

---

## 2. Root Cause Explanation
The vulnerable endpoint permits state-changing actions via HTTP `GET` requests, allowing attackers to leverage standard media tags (such as `<img>`, `<script>`, or `<iframe>`) on external websites to forge unauthorized actions using ambient session cookies.

---

## 3. Implemented Mitigation
Implemented a two-layer defense on `/patched`:
1. **Enforced Method Restrictions:** State changes are rejected on `GET` and require `POST`, conforming to RFC 7231 idempotency rules.
2. **Synchronizer Token Validation:** Enforces a per-session Anti-CSRF token checked using `secrets.compare_digest()`.

---

## 4. Alternative Course Mitigations
Beyond synchronizer tokens, course defenses include:
- **SameSite Cookie Attribute:** Setting `SameSite=Lax` or `SameSite=Strict` ensures the browser refuses to send cookies with cross-site image requests.
- **Custom Request Headers:** Requiring AJAX headers (e.g., `X-Requested-With: XMLHttpRequest`), which cannot be set across origins without preflight CORS approval.
- **Re-Authentication for Sensitive Actions:** Requiring confirmation prompts or password re-entry prior to updating sensitive profile state.
