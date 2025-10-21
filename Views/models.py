import os
import sys
import subprocess
import mysql.connector
from datetime import datetime, timedelta, date
import calendar
import os as _os

# DB connect helper

def connect_db():
    """Return DB connection. Uses a short timeout to fail fast if MySQL is down."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prometricdb",
        connection_timeout=3
    )

# Employee helpers

def register_employee(data):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        # support optional security question/answer
        sql = """
            INSERT INTO employee_personal
            (email_id, Name, tutored_subject, center, date_joined, password, role, security_question, security_answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        sec_q = data.get("security_question")
        sec_a = data.get("security_answer")
        sec_answer = sec_a if sec_a else None
        values = (
            data["email"],
            data["full_name"],
            data.get("tutored_subject"),
            data.get("center"),
            data.get("date_joined"),
            data.get("password"),
            data.get("role"),
            sec_q,
            sec_answer
        )
        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Registration Error:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def login_employee(email_id, password):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT employee_id FROM employee_personal WHERE email_id = %s AND password = %s",
            (email_id, password)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("login_employee error:", e)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
def get_employee_id_by_email(email):
    # return id for an email
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT employee_id FROM employee_personal WHERE email_id = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_employee_id_by_name(name):
    # lookup id by name
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT employee_id FROM employee_personal WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_employee_details(emp_id):
    # name, role
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT Name, role FROM employee_personal WHERE employee_id = %s"
    cursor.execute(sql, (emp_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_employee_overall_rating(employee_id):
    # avg rating from student_feedback
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ROUND(AVG(rating), 2)
            FROM student_feedback
            WHERE employee_id = %s
        """, (employee_id,))
        result = cursor.fetchone()
        return result[0] if result and result[0] else 0.0
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_employee_task_efficiency(employee_id):
    # avg task efficiency
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ROUND(AVG(task_efficiency), 2)
            FROM student_feedback
            WHERE employee_id = %s
        """, (employee_id,))
        result = cursor.fetchone()
        return result[0] if result and result[0] else 0.0
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_employee_overall_rating(emp_id):
    # avg final_score from ratings
    conn = connect_db()
    cursor = conn.cursor()
    sql = """
        SELECT AVG(final_score)
        FROM ratings
        WHERE employee_id = %s
    """
    cursor.execute(sql, (emp_id,))
    result = cursor.fetchone()
    conn.close()
    return round(result[0], 2) if result[0] else 0.0

def get_employee_review_months(emp_id):
    # months with feedback: include ratings + student_feedback
    conn = connect_db()
    cursor = conn.cursor()
    sql = """
        SELECT DISTINCT month FROM (
            SELECT DATE_FORMAT(submitted_on, '%Y-%m') AS month
            FROM ratings
            WHERE employee_id = %s
            UNION
            SELECT DATE_FORMAT(submitted_on, '%Y-%m') AS month
            FROM student_feedback
            WHERE employee_id = %s
        ) AS months
        ORDER BY month DESC
    """
    cursor.execute(sql, (emp_id, emp_id))
    months = [row[0] for row in cursor.fetchall()]
    conn.close()
    return months


def get_employee_rating_by_month(emp_id, month_str):
    # average metrics for a month
    conn = connect_db()
    cursor = conn.cursor()
    sql = """
        SELECT
            AVG(student_feedback),
            AVG(task_efficiency),
            AVG(engagement_level),
            AVG(use_of_examples),
            AVG(adaptability),
            AVG(after_class_responsiveness),
            AVG(confidence_boost),
            AVG(final_score)
        FROM ratings
        WHERE employee_id = %s
        AND DATE_FORMAT(submitted_on, '%Y-%m') = %s
    """
    cursor.execute(sql, (emp_id, month_str))
    result = cursor.fetchone()
    conn.close()
    return result

def get_all_student_feedback_for_employee(employee_id):
    # fetch all student_feedback rows for employee
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT rating, task_efficiency, comment, submitted_on
            FROM student_feedback
            WHERE employee_id = %s
        """, (employee_id,))
        return cursor.fetchall()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def insert_default_ratings(employee_id, session_id, role):
    # create starter ratings for new employee (skip managers)
    conn, cursor = None, None
    try:
        if role.lower() == "manager":
            return True

        conn = connect_db()
        cursor = conn.cursor()

        student_feedback = 7.5
        peer_review = 8.0
        task_efficiency = 7.0
        attendance = 8.0
        upskilling = 7.5
        final_score = round((student_feedback + peer_review + task_efficiency + attendance + upskilling) / 5, 2)

        sql = """
            INSERT INTO ratings
            (employee_id, manager_id, session_id,
             student_feedback, peer_review, task_efficiency,
             attendance, upskilling, final_score, comments, submitted_on)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        values = (
            employee_id,
            1,
            session_id,
            student_feedback,
            peer_review,
            task_efficiency,
            attendance,
            upskilling,
            final_score,
            "Initial auto-generated rating"
        )
        cursor.execute(sql, values)
        conn.commit()
        return True
    except Exception as e:
        print("Error inserting default ratings:", e)
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def create_review_session(employee_id):
    # insert a 30-day review session
    try:
        conn = connect_db()
        cursor = conn.cursor()
        today = date.today()
        end_date = today + timedelta(days=30)

        sql = """
            INSERT INTO review_sessions (start_date, end_date, is_active)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (
            today.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            1
        ))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Error creating review session:", e)
        return None
    finally:
        cursor.close()
        conn.close()
        
def launch_employee_registration(root):
    # open employee registration
    root.destroy()
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'employee_registration.py'))
    subprocess.Popen([sys.executable, dashboard_path])

def launch_employee_login(root):
    # open employee login
    root.destroy()
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'employee_login.py'))
    subprocess.Popen([sys.executable, dashboard_path])
    
def launch_employee_dashboard(email_id):
    # launch employee dashboard with id
    emp_id = get_employee_id_by_email(email_id)
    print("Launching dashboard for employee_id:", emp_id)
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'employee_dashboard.py'))
    subprocess.Popen([sys.executable, dashboard_path, str(emp_id)]) 
    
# ==================================================
# STUDENT FUNCTIONS
# ==================================================

def register_student(data):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = """
            INSERT INTO student (name, email, phone, course, center, password, security_question, security_answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        sec_q = data.get("security_question")
        sec_a = data.get("security_answer")
        sec_answer = sec_a if sec_a else None
        values = (
            data["full_name"], data["email"], data.get("phone"),
            data.get("course"), data.get("center"), data.get("password"),
            sec_q, sec_answer
        )
        cursor.execute(sql, values)
        conn.commit()
        return True
    except Exception as e:
        print("Student Registration Error:", e)
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def login_student(email, password):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT email FROM student WHERE email = %s AND password = %s",
            (email, password)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("Student Login Error:", e)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
def get_student_dashboard_data(student_id):
    """
    Returns:
      {
        "name": ...,
        "course": ...,
        "pending_count": int,    # pending for current month
        "completed_count": int,  # completed this month
        "tutors": [names]        # tutors not yet rated this month
      }
    """
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        # get student basic info
        cursor.execute("SELECT name, course FROM student WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            return None

        # count completed ratings for current month
        # use student_feedback table which now gets a row when a student rates
        cursor.execute("""
            SELECT COUNT(*) AS completed
            FROM student_feedback
            WHERE student_id = %s
              AND DATE_FORMAT(submitted_on, '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')
        """, (student_id,))
        completed = cursor.fetchone()["completed"]

        # total tutors matching student's courses
        total_tutors = get_total_tutors_for_student(student_id)

        # pending for this month
        pending = max(total_tutors - completed, 0)

        # build list of tutor names that match student's course and NOT rated by this student in current month
        course_list = [c.strip() for c in (student["course"] or "").split(",") if c.strip()]
        tutors = []

        if course_list:
            # prepare clauses for subjects
            where_clause = ' OR '.join(['LOWER(ep.tutored_subject) LIKE %s' for _ in course_list])
            params = [f"%{c.lower()}%" for c in course_list]

            # Exclude employee_ids the student has rated in current month
            # fetch employee ids rated by this student this month
            cursor.execute("""
                SELECT DISTINCT employee_id
                FROM student_feedback
                WHERE student_id = %s
                  AND DATE_FORMAT(submitted_on, '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')
            """, (student_id,))
            rated_ids = set(r["employee_id"] for r in cursor.fetchall())

            # Now fetch matching tutors and filter client-side by rated_ids (safe and simple)
            cursor.execute(f"""
                SELECT DISTINCT ep.employee_id, ep.Name, ep.tutored_subject
                FROM employee_personal ep
                WHERE ({where_clause})
                ORDER BY ep.Name
            """, tuple(params))
            rows = cursor.fetchall()
            for row in rows:
                emp_id = row["employee_id"]
                name = row["Name"]
                if emp_id not in rated_ids:
                    tutors.append(name)

        return {
            "name": student["name"],
            "course": student["course"],
            "pending_count": pending,
            "completed_count": completed,
            "tutors": tutors
        }
    except Exception as e:
        print("Dashboard data error:", e)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_completed_count(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*)
        FROM student_feedback
        WHERE student_id = %s
        AND MONTH(submitted_on) = MONTH(CURRENT_DATE())
        AND YEAR(submitted_on) = YEAR(CURRENT_DATE())
    """
    cursor.execute(query, (student_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def submit_rating(student_id, employee_id, rating, comment, task_efficiency):
    """Insert a student rating into the database."""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO student_feedback (
                student_id,
                employee_id,
                rating,
                comment,
                submitted_on,
                task_efficiency
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            student_id,
            employee_id,
            rating,
            comment,
            datetime.now(),
            task_efficiency
        ))
        conn.commit()
    except Exception as e:
        print(f"Error inserting rating: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
        
def get_student_id_by_email(email):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT student_id FROM student WHERE email = %s",
            (email,)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("get_student_id_by_email error:", e)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_student_details(student_id):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, course FROM student WHERE student_id = %s",
            (student_id,)
        )
        return cursor.fetchone()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_student_courses(student_id):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT course FROM student WHERE student_id = %s",
            (student_id,)
        )
        result = cursor.fetchone()
        if result and result[0]:
            return [c.strip().lower() for c in result[0].split(",")]
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_total_tutors_for_student(student_id):
    conn, cursor = None, None
    try:
        student_subjects = get_student_courses(student_id)
        if not student_subjects:
            return 0

        conn = connect_db()
        cursor = conn.cursor()

        like_clauses = " OR ".join(["LOWER(tutored_subject) LIKE %s" for _ in student_subjects])
        query = f"""
            SELECT COUNT(*) 
            FROM employee_personal
            WHERE {like_clauses}
        """
        params = [f"%{sub}%" for sub in student_subjects]

        cursor.execute(query, tuple(params))
        return cursor.fetchone()[0]
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_pending_tutor_list(student_id, return_all=False):
    conn = None
    cursor = None
    try:
        student_subjects = get_student_courses(student_id)
        if not student_subjects:
            return []

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        # all employees matching any subject
        like_clauses = " OR ".join(["LOWER(tutored_subject) LIKE %s" for _ in student_subjects])
        params = tuple([f"%{s}%" for s in student_subjects])
        cursor.execute(f"""
            SELECT employee_id, Name, tutored_subject
            FROM employee_personal
            WHERE {like_clauses}
            ORDER BY Name
        """, params)
        all_employees = cursor.fetchall()

        # find employee_ids rated by this student THIS MONTH
        cursor.execute("""
            SELECT DISTINCT employee_id FROM student_feedback
            WHERE student_id = %s
              AND DATE_FORMAT(submitted_on, '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')
        """, (student_id,))
        rated_ids = set(row["employee_id"] for row in cursor.fetchall())

        filtered = []
        for row in all_employees:
            emp_id = row["employee_id"]
            name = row["Name"]
            if return_all or emp_id not in rated_ids:
                filtered.append((emp_id, name))

        return filtered
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_pending_tutors(student_id):
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT course FROM student WHERE student_id = %s", (student_id,))
        row = cursor.fetchone()
        if not row or not row.get('course'):
            return []

        # normalize course list and build LIKE params
        student_subjects = [c.strip() for c in row['course'].split(',') if c.strip()]
        if not student_subjects:
            return []

        like_clauses = " OR ".join(["LOWER(tutored_subject) LIKE %s" for _ in student_subjects])
        params = tuple([f"%{s.lower()}%" for s in student_subjects])

        cursor.execute(f"""
            SELECT employee_id, Name, tutored_subject
            FROM employee_personal
            WHERE {like_clauses}
            ORDER BY Name
        """, params)
        tutors = cursor.fetchall()

        # find employee_ids rated by this student THIS MONTH
        cursor.execute("""
            SELECT DISTINCT employee_id FROM student_feedback
            WHERE student_id = %s
              AND DATE_FORMAT(submitted_on, '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')
        """, (student_id,))
        rated_ids = {r['employee_id'] for r in cursor.fetchall()}

        pending = []
        for t in tutors:
            if t['employee_id'] not in rated_ids:
                pending.append({'id': t['employee_id'], 'Name': t['Name'], 'tutored_subject': t.get('tutored_subject')})

        return pending
    except Exception as e:
        print("Error in get_pending_tutors:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def count_student_feedback(student_id):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM student_feedback WHERE student_id = %s",
            (student_id,)
        )
        completed = cursor.fetchone()[0]

        total_tutors = get_total_tutors_for_student(student_id)
        pending = max(total_tutors - completed, 0)

        return total_tutors, pending, completed
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_student_feedbacks(emp_id):
    conn = connect_db()
    cursor = conn.cursor()
    sql = """
        SELECT comments
        FROM ratings
        WHERE employee_id = %s
        AND comments IS NOT NULL
        AND comments <> ''
    """
    cursor.execute(sql, (emp_id,))
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]

def launch_student_registration(root):
    root.destroy()
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'student_registration.py'))
    subprocess.Popen([sys.executable, dashboard_path])

def launch_student_login(root):
    root.destroy()
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'student_login.py'))
    subprocess.Popen([sys.executable, dashboard_path])

def launch_host(root=None):
    """Close current window (if provided) and open the main host/home screen.

    Accepts an optional `root` so callers don't have to pass the current Tk root
    (the back-button handler already destroys the top-level window).
    """
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'host.py'))
    subprocess.Popen([sys.executable, dashboard_path])

def make_back_button(parent, launcher_func, launcher_args=None, text='\u2190 Back'):
    """
    Create and return a small back button placed in the top-left corner of `parent`.

    - parent: a tkinter widget (Frame or root)
    - launcher_func: function in models.py that accepts the root and launches a target screen
    - launcher_args: tuple of args to pass to launcher_func (optional)
    - text: label for the button (default: '← Back')

    The button destroys the current root (if available via parent.winfo_toplevel()) and calls launcher_func.
    """
    import tkinter as tk

    def on_back():
        # Best-effort: destroy the current top-level first, then call launcher
        # in a background thread to avoid race conditions where both the
        # current window and the target window appear together.
        try:
            root = parent.winfo_toplevel()
        except Exception:
            root = None

        # destroy current window first
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass

        # invoke launcher in background so we don't depend on the destroyed root
        import threading

        def _call_launcher():
            try:
                if launcher_args:
                    launcher_func(*launcher_args)
                else:
                    launcher_func()
            except Exception as e:
                # don't crash the UI; print error for debugging
                print("Back button launcher error:", e)

        t = threading.Thread(target=_call_launcher, daemon=True)
        t.start()

    btn = tk.Button(parent, text=text, font=("Arial", 10), bg="white", bd=0, fg="#0b5394", activebackground="white", command=on_back)
    # place so it looks like a corner control; caller can reposition if needed
    try:
        btn.place(x=10, y=10)
    except Exception:
        pass
    return btn
# ==================================================
# MANAGER FUNCTIONS
# ==================================================
def register_manager(data):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = """
            INSERT INTO managers (email_id, name, tutored_subject, center, password, security_question, security_answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        sec_q = data.get("security_question")
        sec_a = data.get("security_answer")
        sec_answer = sec_a if sec_a else None
        cursor.execute(sql, (
            data["email"],
            data["full_name"],
            data.get("tutored_subject"),   # might be empty
            data.get("center"),
            data.get("password"),
            sec_q,
            sec_answer
        ))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Manager registration error:", e)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def login_manager(email_id, password):
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM managers WHERE email_id = %s AND Password = %s",
            (email_id, password)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_manager_details(manager_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM managers WHERE email_id = %s",
            (manager_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else "Unknown"
    except Exception as e:
        print("Error fetching manager:", e)
        return "Unknown"
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
def get_all_employee_feedbacks():
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                e.employee_id,
                e.Name,
                e.tutored_subject,
                s.rating,
                s.comment
            FROM
                employee_personal e
                LEFT JOIN student_feedback s ON e.employee_id = s.employee_id
            ORDER BY e.Name
        """)
        return cursor.fetchall()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
def launch_manager_login(root):
    root.destroy()
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'manager_login.py'))
    subprocess.Popen([sys.executable, dashboard_path])

        
def launch_manager_dashboard(root):
    root.destroy()
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'manager_dashboard.py'))
    subprocess.Popen([sys.executable, dashboard_path])

def get_total_employees():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM employee_personal")
        return cursor.fetchone()[0]
    except:
        return 0
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_total_student():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM student_feedback")
        return cursor.fetchone()[0]
    except:
        return 0
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_employee_leaderboard():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        # include all tutors, avg_rating may be NULL if no ratings yet
        cursor.execute("""
            SELECT ep.Name, ROUND(AVG(r.final_score), 2) as avg_rating
            FROM employee_personal ep
            LEFT JOIN ratings r ON ep.employee_id = r.employee_id
            GROUP BY ep.employee_id
            ORDER BY (AVG(r.final_score) IS NULL) ASC, AVG(r.final_score) DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error loading leaderboard:", e)
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ==================================================
# SHARED FUNCTIONS / UTILITIES
# ==================================================

def submit_student_feedback(data):
    """
    Insert a detailed ratings row (ratings table) AND a compact student_feedback row
    so dashboard logic that checks student_feedback continues to work.

    Expected keys in data:
      - employee_id (int)
      - student_id (int)    <-- MUST be provided
      - manager_id (int)
      - session_id (int)
      - student_feedback (float)         # overall rating given by student
      - task_efficiency (float)
      - engagement_level (float)
      - use_of_examples (float)
      - adaptability (float)
      - after_class_responsiveness (float)
      - confidence_boost (float)
      - comment (string)
      - submitted_on (datetime)  (optional; if missing will use NOW())
    """
    if "student_id" not in data:
        raise ValueError("submit_student_feedback requires 'student_id' in data")

    conn = connect_db()
    cursor = conn.cursor()

    sql_ratings = """
        INSERT INTO ratings (
            employee_id,
            manager_id,
            session_id,
            student_feedback,
            task_efficiency,
            engagement_level,
            use_of_examples,
            adaptability,
            after_class_responsiveness,
            confidence_boost,
            final_score,
            comments,
            submitted_on
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # compute final_score as average of the 7 student metrics (if all present)
    metric_values = [
        data.get("student_feedback", 0),
        data.get("task_efficiency", 0),
        data.get("engagement_level", 0),
        data.get("use_of_examples", 0),
        data.get("adaptability", 0),
        data.get("after_class_responsiveness", 0),
        data.get("confidence_boost", 0)
    ]

    # avoid division by zero; count only metrics that are numeric (non-None)
    valid_metrics = [v for v in metric_values if v is not None]
    final_score = round(sum(valid_metrics) / len(valid_metrics), 2) if valid_metrics else 0.0

    submitted_on = data.get("submitted_on")
    if submitted_on is None:
        submitted_on = datetime.now()

    values_ratings = (
        data["employee_id"],
        data.get("manager_id", 1),
        data.get("session_id", None),
        data.get("student_feedback"),
        data.get("task_efficiency"),
        data.get("engagement_level"),
        data.get("use_of_examples"),
        data.get("adaptability"),
        data.get("after_class_responsiveness"),
        data.get("confidence_boost"),
        final_score,
        data.get("comment"),
        submitted_on
    )

    # Insert into ratings table
    cursor.execute(sql_ratings, values_ratings)
    conn.commit()

    # Also insert a simplified row into student_feedback so the student dashboard and
    # other parts of the app (which rely on student_feedback) see the rating immediately.
    # Use overall student_feedback metric as rating if present (fallback to final_score).
    rating_value = data.get("student_feedback", final_score)
    task_eff = data.get("task_efficiency", None)

    sql_student_feedback = """
        INSERT INTO student_feedback (
            student_id,
            employee_id,
            rating,
            task_efficiency,
            comment,
            submitted_on
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values_sf = (
        data["student_id"],
        data["employee_id"],
        rating_value,
        task_eff,
        data.get("comment"),
        submitted_on
    )

    cursor.execute(sql_student_feedback, values_sf)
    conn.commit()

    cursor.close()
    conn.close()


def get_review_periods():
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, start_date, end_date, is_active
            FROM review_sessions
            ORDER BY start_date DESC
        """)
        rows = cursor.fetchall()
        return [(row["id"], row["start_date"]) for row in rows]
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
# ---------------- REVIEW SESSION HELPERS ---------------- #

def ensure_review_sessions_exist():
    """
    Creates review periods from earliest feedback date up to current month.
    """
    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MIN(submitted_on)
            FROM student_feedback
        """)
        result = cursor.fetchone()
        earliest_date = result[0]

        if not earliest_date:
            return

        current_month_start = datetime(earliest_date.year, earliest_date.month, 1)
        today = datetime.today()
        while current_month_start <= today:
            month_end_day = calendar.monthrange(current_month_start.year, current_month_start.month)[1]
            start_date = current_month_start.strftime("%Y-%m-%d")
            end_date = current_month_start.replace(day=month_end_day).strftime("%Y-%m-%d")

            cursor.execute("""
                SELECT COUNT(*) FROM review_sessions
                WHERE start_date = %s AND end_date = %s
            """, (start_date, end_date))
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute("""
                    INSERT INTO review_sessions (start_date, end_date, is_active)
                    VALUES (%s, %s, %s)
                """, (start_date, end_date, 0))

            # Move to next month
            if current_month_start.month == 12:
                current_month_start = datetime(current_month_start.year + 1, 1, 1)
            else:
                current_month_start = datetime(
                    current_month_start.year, current_month_start.month + 1, 1
                )

        conn.commit()

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def ensure_current_month_review_session():
    """
    Ensures a review session exists for the current month.
    """
    today = datetime.today()
    start_date = today.replace(day=1).strftime("%Y-%m-%d")
    end_day = calendar.monthrange(today.year, today.month)[1]
    end_date = today.replace(day=end_day).strftime("%Y-%m-%d")

    conn, cursor = None, None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM review_sessions
            WHERE start_date = %s AND end_date = %s
        """, (start_date, end_date))
        exists = cursor.fetchone()[0]

        if not exists:
            cursor.execute("""
                INSERT INTO review_sessions (start_date, end_date, is_active)
                VALUES (%s, %s, %s)
            """, (start_date, end_date, 1))
            conn.commit()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def save_improvement_suggestion(name, email, message):
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
        INSERT INTO improvements (name, email, message)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (name, email, message))
    conn.commit()
    conn.close()
    
def launch_suggest_improvement(root):
    root.destroy()
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'suggest_improvement.py'))
    subprocess.Popen([sys.executable, dashboard_path])


def verify_user_by_name_email(user_type, first_name, last_name, email):
    """Return tuple (user_id, table_name) if a user matches first+last+email (case-insensitive).
    user_type: 'student', 'employee', or 'manager' - selects table and id column.
    """
    table_map = {
        'student': ('student', 'student_id', ['name', 'email']),
        'employee': ('employee_personal', 'employee_id', ['Name', 'email_id']),
        'manager': ('managers', 'id', ['name', 'email_id'])
    }
    if user_type not in table_map:
        return None

    table, id_col, cols = table_map[user_type]
    # We'll match by splitting stored name into first/last and comparing case-insensitive
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # normalize inputs
        email_l = email.strip().lower()
        first_l = first_name.strip().lower()
        last_l = last_name.strip().lower()

        # fetch candidates with matching email and include the security question
        sql = f"SELECT {id_col}, {cols[0]} as full_name, {cols[1]} as email, security_question FROM {table} WHERE LOWER({cols[1]}) = %s"
        cursor.execute(sql, (email_l,))
        for row in cursor.fetchall():
            uid = row[id_col]
            full = row.get('full_name') or ''
            parts = [p.strip().lower() for p in full.split() if p.strip()]
            # check first and last anywhere in the split parts
            if not parts:
                continue
            if first_l in parts and last_l in parts:
                # Return id, table and the stored security question (may be None)
                return (uid, table, row.get('security_question'))
        return None
    finally:
        cursor.close()
        conn.close()


def verify_security_answer(user_type, user_id, answer_plain):
    """Return True if the provided answer matches the stored plain-text answer
    for (user_type, user_id).
    """
    table_map = {
        'student': ('student', 'student_id'),
        'employee': ('employee_personal', 'employee_id'),
        'manager': ('managers', 'id')
    }
    if user_type not in table_map:
        return False

    table, id_col = table_map[user_type]
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = f"SELECT security_answer FROM {table} WHERE {id_col} = %s"
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        if not row or not row[0]:
            return False
        stored = row[0]
        # compare case-insensitive trimmed answers
        return str(stored).strip().lower() == str(answer_plain).strip().lower()
    except Exception as e:
        print('verify_security_answer error:', e)
        return False
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def set_security_answer(user_type, user_id, question, answer_plain):
    """Set (or update) the security question and plain-text answer for a user.

    Returns True on success, False on error.
    """
    table_map = {
        'student': ('student', 'student_id'),
        'employee': ('employee_personal', 'employee_id'),
        'manager': ('managers', 'id')
    }
    if user_type not in table_map:
        return False

    table, id_col = table_map[user_type]
    plain_answer = str(answer_plain).strip() if answer_plain else None
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = f"UPDATE {table} SET security_question = %s, security_answer = %s WHERE {id_col} = %s"
        cursor.execute(sql, (question, plain_answer, user_id))
        conn.commit()
        return True
    except Exception as e:
        print('set_security_answer error:', e)
        try:
            if conn:
                conn.rollback()
        except Exception:
            pass
        return False
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def get_security_fields(user_type, user_id):
    """Return a tuple (security_question, security_answer) for the given user, or (None, None)."""
    table_map = {
        'student': ('student', 'student_id'),
        'employee': ('employee_personal', 'employee_id'),
        'manager': ('managers', 'id')
    }
    if user_type not in table_map:
        return (None, None)

    table, id_col = table_map[user_type]
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = f"SELECT security_question, security_answer FROM {table} WHERE {id_col} = %s"
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        if not row:
            return (None, None)
        return (row[0], row[1])
    except Exception as e:
        print('get_security_fields error:', e)
        return (None, None)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def update_password(user_type, user_id, new_password):
    """Update password for a user. Returns True on success."""
    table_map = {
        'student': ('student', 'student_id', 'password'),
        'employee': ('employee_personal', 'employee_id', 'password'),
        'manager': ('managers', 'id', 'Password')
    }
    if user_type not in table_map:
        return False

    table, id_col, pwd_col = table_map[user_type]
    conn = connect_db()
    cursor = conn.cursor()
    try:
        sql = f"UPDATE {table} SET {pwd_col} = %s WHERE {id_col} = %s"
        cursor.execute(sql, (new_password, user_id))
        conn.commit()
        return True
    except Exception as e:
        print('update_password error:', e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def launch_forgot_password(root):
    try:
        root.destroy()
    except Exception:
        pass
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views', 'forgot_password.py'))
    subprocess.Popen([sys.executable, dashboard_path])