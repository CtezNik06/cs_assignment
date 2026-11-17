# Member 1: Mayank Anand - SQL Injection (In-Band Authentication Bypass)

## 1. How to Run & Reproduce

### Prerequisites
- Python 3.8+
- Flask & Requests (`pip install flask requests`)

### Steps:
1. **Start the Flask Application:**
   ```bash
   cd member1_sqli
   python app.py
   ```
   The application runs at `http://127.0.0.1:5001/`.

2. **Manual Exploit Reproduction:**
   - Navigate to `http://127.0.0.1:5001/` in your web browser.
   - In the **Vulnerable Login** form, input:
     - **Username:** `admin' --`
     - **Password:** `anything`
   - Click **Login (Vulnerable Path)**.
   - Observe the authentication bypass: You are logged in as the Administrator without knowing the password.

3. **Verify the Patch:**
   - In the **Patched Login** form, submit the identical payload (`admin' --`).
   - Click **Login (Patched Path)**.
   - The system returns `Access Denied: Invalid credentials`, neutralizing the attack.

4. **Automated Exploit Execution:**
   ```bash
   python exploit.py
   ```

---

## 2. Root Cause Explanation
The vulnerable endpoint (`/vuln`) dynamically constructs SQL queries using untrusted user input via Python f-string formatting (`f"SELECT ... '{username}'"`), allowing attacker-controlled quotes to escape data context and alter query structure.

---

## 3. Implemented Mitigation
Implemented **Parameterized Queries (Prepared Statements)** on `/patched` using `cursor.execute("SELECT ... WHERE username = ? AND password = ?", (username, password))`. The database engine compiles the SQL command structure prior to binding user inputs, ensuring parameters are interpreted strictly as literal values.

---

## 4. Alternative Course Mitigations
Beyond parameterized queries, enterprise architectures defend against SQL injection via:
- **Object-Relational Mapping (ORM) Frameworks:** Modern frameworks (such as SQLAlchemy, Hibernate, or Django ORM) automatically abstract SQL generation using parameterized queries by default.
- **Stored Procedures:** Storing parameterized procedures on the database server decouples business logic from dynamic input construction, maintaining execution plan isolation.
- **Strict Input Allowlisting & Validation:** Rejecting unexpected characters (e.g., single quotes, double hyphens) at the API boundary, coupled with the Principle of Least Privilege (granting the database user read-only access to necessary tables).
