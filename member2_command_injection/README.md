# Member 2: D. RadhaKrishna - OS Command Injection (Direct Shell Concatenation)

## 1. How to Run & Reproduce

### Prerequisites
- Python 3.8+
- Flask & Requests (`pip install flask requests`)

### Steps:
1. **Start the Diagnostic Server:**
   ```bash
   cd member2_command_injection
   python app.py
   ```
   Application runs on `http://127.0.0.1:5002/`.

2. **Manual Exploit Reproduction:**
   - Open `http://127.0.0.1:5002/` in a browser.
   - In the **Vulnerable Diagnostic Tool** form, input:
     - `127.0.0.1 && whoami` (Windows/Linux)
   - Click **Run Diagnostic (Vulnerable Path)**.
   - Observe that system user identity is dumped directly into the output terminal block.

3. **Verify the Patch:**
   - In the **Patched Diagnostic Tool** form, submit the identical payload (`127.0.0.1 && whoami`).
   - Click **Run Diagnostic (Patched Path)**.
   - The application immediately responds with `[SECURITY ERROR] Rejected: Target contains disallowed shell metacharacters`.

4. **Automated Exploit Execution:**
   ```bash
   python exploit.py
   ```

---

## 2. Root Cause Explanation
The vulnerable endpoint (`/vuln`) passes unsanitized user strings into the operating system command shell via `shell=True`, allowing command chaining operators (`&&`, `;`, `|`) to execute arbitrary secondary system binaries under the web server's privilege level.

---

## 3. Implemented Mitigation
Implemented a two-layer defense on `/patched`:
1. **Structured Execution (`shell=False`):** Commands are invoked as discrete argument lists (`["ping", "-n", "1", target]`), eliminating shell evaluation.
2. **Strict Regex Allowlisting:** Targets must match `^[a-zA-Z0-9.-]+$`, outright rejecting any shell metacharacters before execution.

---

## 4. Alternative Course Mitigations
Beyond structured parameter arrays, defensive architectures employ:
- **Direct Programming Language APIs:** Utilizing native runtime networking libraries (such as Python's `socket` or `urllib`) rather than shelling out to OS system binaries.
- **Privilege Separation & Sandboxing:** Executing web server processes under unprivileged service accounts or inside containerized jail environments (e.g., AppArmor, seccomp, Docker containers) with restricted binary paths.
- **System Command Whitelisting:** Using tools like `sudoers` or custom execution wrappers that restrict execution to specific known-safe scripts with non-configurable flags.
