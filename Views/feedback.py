import tkinter as tk
from tkinter import messagebox, ttk
import sys
from datetime import datetime
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

if len(sys.argv) < 3:
    messagebox.showerror("Error", "Tutor name or student ID missing!")
    sys.exit()

tutor_name = sys.argv[1]
student_id = int(sys.argv[2])

root = tk.Tk()
root.title("Tutor Feedback")
root.geometry("500x700")
root.config(bg="white")

# back button to host
try:
    ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
except Exception:
    pass

tk.Label(root, text=f"Rate Tutor: {tutor_name}", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

rating_fields = {
    "student_feedback": "Overall Rating (1-5)",
    "task_efficiency": "Task Efficiency (1-5)",
    "engagement_level": "Engagement Level (1-5)",
    "use_of_examples": "Use of Examples (1-5)",
    "adaptability": "Adaptability (1-5)",
    "after_class_responsiveness": "After Class Responsiveness (1-5)",
    "confidence_boost": "Confidence Boost (1-5)"
}

variables = {}
for key, label in rating_fields.items():
    tk.Label(root, text=label, bg="white").pack(pady=(10, 0))
    var = tk.DoubleVar()
    tk.Entry(root, textvariable=var, width=5).pack()
    variables[key] = var

tk.Label(root, text="Comments:", bg="white").pack(pady=(10, 0))
comment_frame = tk.Frame(root, bg="white")
comment_frame.pack()
comment_box = tk.Text(comment_frame, width=50, height=5, wrap="word", relief="solid", bd=1)
comment_box.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(comment_frame, orient="vertical", command=comment_box.yview)
scrollbar.pack(side="right", fill="y")
comment_box.config(yscrollcommand=scrollbar.set)

def submit_rating():
    ratings = {}
    for key, var in variables.items():
        val = var.get()
        if not (1 <= val <= 5):
            messagebox.showwarning("Invalid Input", f"Please enter a value between 1 and 5 for {key.replace('_',' ').title()}.")
            return
        ratings[key] = val

    comment = comment_box.get("1.0", tk.END).strip()
    emp_id = ml.get_employee_id_by_name(tutor_name)
    if not emp_id:
        messagebox.showerror("Error", "Tutor not found in database.")
        return

    data = {
        "student_feedback": ratings["student_feedback"],
        "task_efficiency": ratings["task_efficiency"],
        "engagement_level": ratings["engagement_level"],
        "use_of_examples": ratings["use_of_examples"],
        "adaptability": ratings["adaptability"],
        "after_class_responsiveness": ratings["after_class_responsiveness"],
        "confidence_boost": ratings["confidence_boost"],
        "employee_id": emp_id,
        "student_id": student_id, 
        "manager_id": 1,  # default or pass via arguments
        "session_id": 1,  # default or pass via arguments
        "comment": comment,
        "submitted_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    }

    ml.submit_student_feedback(data)
    messagebox.showinfo("Success", f"Feedback submitted for {tutor_name}!")
    root.destroy()

tk.Button(
    root,
    text="Submit Feedback",
    command=submit_rating,
    bg="#0b5394",
    fg="white"
).pack(pady=20)

root.mainloop()