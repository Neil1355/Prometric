# ProMetric Tutoring System

A compact, local desktop application for managing students, tutors (employees), and managers. ProMetric collects improvement suggestions, handles registrations, and provides a small dashboard-driven workflow for staff.

---

## Quick start — run the app locally

Prerequisites

- Python 3.10+ (recommended)
- MySQL server (local) with an accessible user
- Git (optional) and a terminal (PowerShell on Windows)

Steps (PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r ..\requirements.txt
```

3. Ensure the database exists and credentials are correct

- The app defaults to: host=localhost, user=root, password='', database=prometricdb.
- If `prometricdb` doesn't exist, create it in MySQL:

```sql
CREATE DATABASE prometricdb;
```

4. Start the app (from the `Views/` folder)

```powershell
cd Views
python host.py
```

Notes

- This is a desktop Tkinter app — it is not a web server. The app connects to a local MySQL instance ("localhost") for data storage.
- If you use different DB credentials, update the `connect_db()` function in `Views/models.py`.

---

## Folder structure (overview)

Root of this workspace (relevant parts):

```
Views/
  host.py                      # Main entry screen (launch this to start the app)
  models.py                    # DB access and app helper functions
  student_registration.py      # Student registration UI
  Student_registration.py      # (alternate student registration view)
  student_login.py             # Student login UI
  student_dashboard.py         # Student dashboard UI
  employee_registration.py     # Employee (tutor) registration UI
  employee_login.py            # Employee login UI
  employee_dashboard.py        # Employee dashboard UI
  manager_login.py             # Manager login UI
  manager_dashboard.py         # Manager dashboard UI
  feedback.py                  # Feedback / suggestion UI
  suggest_improvement.py       # Improvement suggestion UI
  Prometric Logo.png           # Branding / images
  login_bg.jpg                 # Background image used across login forms
  migrations/                  # SQL migration files and helper scripts
    001_add_security_q.sql
    set_security_answer_plain.py
```

Notes

- The `Views/` folder contains both UI code and model helpers; when editing DB code prefer `Views/models.py` for centralized DB logic.
- Image files used by the UI live alongside the view files.

---

## Developer notes and common commands

- Entry point: `Views/host.py`
- DB helper: `Views/models.py`
- To run the UI from the project root:

```powershell
cd Views
python host.py
```

- To backfill a user's security Q/A (manual):

```powershell
python migrations\set_security_answer_plain.py --user_type student --user_id 123 --question "Mother's maiden name" --answer "Smith" --execute
```

---

## Contact

Developer: Neil Barot
 Email: neilbarot5@gmail.com

 Thank You for Using ProMetric - A lightweight, data-driven approach to managing tutoring centers — one metric at a time.
