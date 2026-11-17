# Web Server Vulnerabilities & Defensive Engineering Lab

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Focus-Web%20Security%20%26%20Defenses-red?style=flat&logo=shield)](https://owasp.org/)

A comprehensive university security lab demonstrating real-world web server vulnerabilities, reproducible exploit payloads, root-cause analyses, code-level mitigations, and industry-standard defense-in-depth strategies.

---

## Architecture Strategy: Standalone Folder Structure

To ensure zero merge conflicts and complete modularity, each group member maintains an isolated, self-contained Python Flask application running inside their own directory. Each application includes both a vulnerable route (`/vuln`) and a hardened route (`/patched`).

```text
cs_assignment/
├── .gitignore
├── requirements.txt
├── README.md                           # Main documentation & mapping table
├── member1_sqli/                       # Mayank Anand: SQL Injection (Auth Bypass)
│   ├── app.py                         (Port 5001)
│   ├── exploit.py
│   └── README.md
├── member2_command_injection/         # D. RadhaKrishna: OS Command Injection
│   ├── app.py                         (Port 5002)
│   ├── exploit.py
│   └── README.md
├── member3_xss/                       # Paarth Gupta: Stored Cross-Site Scripting
│   ├── app.py                         (Port 5003)
│   ├── exploit_payload.txt
│   └── README.md
├── member4_csrf_get/                  # Aayushi Bansal: CSRF (GET-based)
│   ├── app.py                         (Port 5004)
│   ├── attacker.html
│   └── README.md
└── member5_csrf_post/                 # Nikhil Goyal: CSRF (POST-based)
    ├── app.py                         (Port 5005)
    ├── attacker.html
    └── README.md
```

---

## Member Vulnerability Distribution Matrix

| Member Name | Assigned Category | Variant | Vulnerable Route | Patched Route | Port |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Mayank Anand** (Member 1) | SQL Injection (SQLi) | In-Band Authentication Bypass | `/vuln` (concatenated SQL) | `/patched` (parameterized queries) | `5001` |
| **D. RadhaKrishna** (Member 2) | OS Command Injection | Direct Shell Concatenation | `/vuln` (`shell=True` execution) | `/patched` (`shell=False` arg list) | `5002` |
| **Paarth Gupta** (Member 3) | Cross-Site Scripting (XSS)| Stored XSS | `/vuln` (raw HTML rendering) | `/patched` (contextual escaping) | `5003` |
| **Aayushi Bansal** (Member 4) | CSRF | GET-based Forged Action | `/vuln` (state mutation via GET) | `/patched` (POST + CSRF token) | `5004` |
| **Nikhil Goyal** (Member 5) | CSRF | POST-based Forged Action | `/vuln` (unverified form POST) | `/patched` (Synchronizer token check) | `5005` |

---

## Quickstart & Setup

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

## Deliverables Overview per Member

Every member module satisfies the assignment requirements:
1. **Identified Vulnerable Code Path**: Clear line-level demonstrations in `app.py`.
2. **Working Exploit Payload**: Reusable test scripts (`exploit.py`) or HTML trigger pages (`attacker.html`).
3. **1-2 Line Root Cause**: Concise identification of the insecure trust boundary.
4. **Code Mitigation**: Direct implementation blocking the identical payload.
5. **Alternative Mitigations**: Theoretical overview covering defense-in-depth principles.

---

## Academic Integrity & Disclaimer
This repository is developed strictly for educational and instructional purposes as part of university coursework in web security. All exploits and vulnerabilities are simulated inside localized testing environments.