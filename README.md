# Web Server Vulnerabilities & Defensive Engineering Lab

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Focus-Web%20Security%20%26%20Defenses-red?style=flat&logo=shield)](https://owasp.org/)

A comprehensive university security lab demonstrating real-world web server vulnerabilities, reproducible exploit payloads, root-cause analyses, code-level mitigations, and industry-standard defense-in-depth strategies.

---

## ðŸ›ï¸ Architecture Strategy: Standalone Folder Structure

To ensure zero merge conflicts and complete modularity, each group member maintains an isolated, self-contained Python Flask application running inside their own directory. Each application includes both a vulnerable route (`/vuln`) and a hardened route (`/patched`).

```text
cs_assignment/
â”œâ”€â”€ .gitignore
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ README.md                           # Main documentation & mapping table
â”œâ”€â”€ member1_sqli/                       # Member 1: SQL Injection (Auth Bypass)
â”‚   â”œâ”€â”€ app.py                         (Port 5001)
â”‚   â”œâ”€â”€ exploit.py
â”‚   â””â”€â”€ README.md
â”œâ”€â”€ member2_command_injection/         # Member 2: OS Command Injection
â”‚   â”œâ”€â”€ app.py                         (Port 5002)
â”‚   â”œâ”€â”€ exploit.py
â”‚   â””â”€â”€ README.md
â”œâ”€â”€ member3_xss/                       # Member 3: Stored Cross-Site Scripting
â”‚   â”œâ”€â”€ app.py                         (Port 5003)
â”‚   â”œâ”€â”€ exploit_payload.txt
â”‚   â””â”€â”€ README.md
â”œâ”€â”€ member4_csrf_get/                  # Member 4: CSRF (GET-based)
â”‚   â”œâ”€â”€ app.py                         (Port 5004)
â”‚   â”œâ”€â”€ attacker.html
â”‚   â””â”€â”€ README.md
â””â”€â”€ member5_csrf_post/                 # Member 5: CSRF (POST-based)
    â”œâ”€â”€ app.py                         (Port 5005)
    â”œâ”€â”€ attacker.html
    â””â”€â”€ README.md
```

---

## ðŸ‘¥ Member Vulnerability Distribution Matrix

| Member | Vulnerability Category | Variant | Vulnerable Route | Patched Route | Port |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Member 1** | SQL Injection (SQLi) | In-Band Authentication Bypass | `/vuln` (concatenated SQL) | `/patched` (parameterized queries) | `5001` |
| **Member 2** | OS Command Injection | Direct Shell Concatenation | `/vuln` (`shell=True` execution) | `/patched` (`shell=False` arg list) | `5002` |
| **Member 3** | Cross-Site Scripting (XSS)| Stored XSS | `/vuln` (raw HTML rendering) | `/patched` (contextual escaping) | `5003` |
| **Member 4** | CSRF | GET-based Forged Action | `/vuln` (state mutation via GET) | `/patched` (POST + CSRF token) | `5004` |
| **Member 5** | CSRF | POST-based Forged Action | `/vuln` (unverified form POST) | `/patched` (Synchronizer token check) | `5005` |

---

## ðŸš€ Quickstart & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/CtezNik06/cs_assignment.git
cd cs_assignment
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Any Member Module
Navigate to any member's directory and launch `app.py`:
```bash
# Example for Member 5:
cd member5_csrf_post
python app.py
```
Refer to the individual `README.md` inside each folder for detailed step-by-step reproduction and verification steps.

---

## ðŸ›¡ï¸ Deliverables Overview per Member

Every member module satisfies the assignment requirements:
1. **Identified Vulnerable Code Path**: Clear line-level demonstrations in `app.py`.
2. **Working Exploit Payload**: Reusable test scripts (`exploit.py`) or HTML trigger pages (`attacker.html`).
3. **1â€“2 Line Root Cause**: Concise identification of the insecure trust boundary.
4. **Code Mitigation**: Direct implementation blocking the identical payload.
5. **Alternative Mitigations**: Theoretical overview covering defense-in-depth principles.

---

## ðŸ“œ Academic Integrity & Disclaimer
This repository is developed strictly for educational and instructional purposes as part of university coursework in web security. All exploits and vulnerabilities are simulated inside localized testing environments.
