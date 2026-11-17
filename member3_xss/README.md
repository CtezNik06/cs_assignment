# Member 3: Paarth Gupta - Cross-Site Scripting (Stored XSS)

## 1. How to Run & Reproduce

### Prerequisites
- Python 3.8+
- Flask (`pip install flask`)

### Steps:
1. **Start the Application:**
   ```bash
   cd member3_xss
   python app.py
   ```
   Application runs on `http://127.0.0.1:5003/`.

2. **Manual Exploit Reproduction:**
   - Open `http://127.0.0.1:5003/` in a web browser.
   - In the **Vulnerable Guestbook** form, paste the following payload:
     ```html
     <script>alert('Stored XSS Vulnerability Confirmed!')</script>
     ```
   - Click **Post Comment (Vulnerable Path)**.
   - Observe that the page reloads and immediately triggers an interactive JavaScript `alert()` dialog. Every visitor viewing this page will execute the attacker's script.

3. **Verify the Patch:**
   - In the **Patched Guestbook** form, submit the identical payload:
     ```html
     <script>alert('Stored XSS Vulnerability Confirmed!')</script>
     ```
   - Click **Post Comment (Patched Path)**.
   - Observe that the script does not execute; the tags are converted into safe HTML entities (`&lt;script&gt;`) and displayed as benign text.

---

## 2. Root Cause Explanation
The vulnerable endpoint stores untrusted user input and renders it directly into the web document using Jinja's `| safe` filter without contextual encoding, allowing browser DOM engines to parse and execute malicious user-supplied JavaScript.

---

## 3. Implemented Mitigation
Implemented **Contextual Context-Aware Output Encoding** using Python's `html.escape()` and default Jinja template escaping. Special characters (`<`, `>`, `&`, `"`, `'`) are converted to their corresponding HTML entities (`&lt;`, `&gt;`, `&amp;`), ensuring the browser interprets the input strictly as textual content rather than executable markup.

---

## 4. Alternative Course Mitigations
Beyond contextual output encoding, defense-in-depth against XSS requires:
- **Content Security Policy (CSP):** Setting restrictive HTTP response headers (e.g., `Content-Security-Policy: default-src 'self'; script-src 'self'`) prevents inline script execution and restricts unauthorized external domain connections.
- **HttpOnly Cookie Flag:** Marking sensitive authentication cookies with the `HttpOnly` directive ensures client-side JavaScript APIs (`document.cookie`) cannot access or steal session tokens even in the event of an XSS flaw.
- **DOMPurify / HTML Sanitizers:** For systems that legitimately require rich text formatting, utilizing rigorous DOM sanitization libraries (e.g., Bleach or DOMPurify) strips out malicious script tags and inline event listeners before storage.
