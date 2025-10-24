import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

# Check argument - make safe for import-time (when running import checks without argv)
emp_id = None
if len(sys.argv) > 1:
    try:
        emp_id = int(sys.argv[1])
    except Exception:
        emp_id = None
if emp_id is None:
    # Running as a module or during import; fall back to a safe sentinel and avoid sys.exit during imports
    emp_id = 1  # default for local testing; adjust as needed

# Fetch employee details
# emp_id = 1  # For testing, replace with actual logic to get emp_id
employee_data = ml.get_employee_details(emp_id)
if not employee_data:
    messagebox.showerror("Error", "Employee not found!")
    sys.exit()

employee_name, employee_role = employee_data
overall_rating = ml.get_employee_overall_rating(emp_id)
months_list = ml.get_employee_review_months(emp_id)

# map YYYY-MM -> "MonthName YYYY" for display
from datetime import datetime as _dt
_display_map = {}
_display_values = []
for m in months_list:
    try:
        d = _dt.strptime(m, "%Y-%m")
        label = d.strftime("%B %Y")
    except Exception:
        label = m
    _display_map[label] = m
    _display_values.append(label)

def on_period_select(event):
    # map displayed label back to YYYY-MM
    selected_label = eval_period_var.get()
    if selected_label:
        selected_month = _display_map.get(selected_label, selected_label)
        rating_data = ml.get_employee_rating_by_month(emp_id, selected_month)
        if rating_data:
            student_feedback = float(rating_data[0] or 0.0)
            task_efficiency = float(rating_data[1] or 0.0)
            engagement_level = float(rating_data[2] or 0.0)
            use_of_examples = float(rating_data[3] or 0.0)
            adaptability = float(rating_data[4] or 0.0)
            after_class_responsiveness = float(rating_data[5] or 0.0)
            confidence_boost = float(rating_data[6] or 0.0)
            final_score_value = float(rating_data[7] or 0.0)

            stu_var.set(str(student_feedback))
            task_var.set(str(task_efficiency))
            engage_var.set(str(engagement_level))
            examples_var.set(str(use_of_examples))
            adapt_var.set(str(adaptability))
            resp_var.set(str(after_class_responsiveness))
            conf_var.set(str(confidence_boost))
            final_var.set(str(final_score_value))
        else:
            stu_var.set("")
            task_var.set("")
            engage_var.set("")
            examples_var.set("")
            adapt_var.set("")
            resp_var.set("")
            conf_var.set("")
            final_var.set("")

def open_feedback_window():
    feedbacks = ml.get_student_feedbacks(emp_id)
    if not feedbacks:
        messagebox.showinfo("No Feedback", "No feedbacks found for this tutor.")
        return

    fb_window = tk.Toplevel(root)
    fb_window.title("Student Feedbacks")
    fb_window.geometry("400x300")
    fb_window.config(bg="white")

    text_box = tk.Text(fb_window, wrap=tk.WORD, width=50, height=15, bg="white")
    text_box.pack(padx=10, pady=10)

    for fb in feedbacks:
        text_box.insert(tk.END, f"- {fb}\n\n")

    tk.Button(fb_window, text="Close", command=fb_window.destroy).pack(pady=10)

root = tk.Tk()
root.title("Tutor Dashboard")
root.geometry("500x700")
root.config(bg="black")

try:
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "Dashboard_bg.jpeg")
    bg_img = Image.open(image_path)
    bg_img = bg_img.resize((500, 700), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo
except Exception as e:
    print("Background image could not be loaded:", e)

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor='center')

# back button to host
try:
    ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
except Exception:
    pass

tk.Label(frame, text="Tutor Performance", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame, text=f"Name: {employee_name}", anchor='w', bg="white").grid(row=1, column=0, sticky='w', pady=5)
tk.Label(frame, text=f"Role: {employee_role}", anchor='w', bg="white").grid(row=1, column=1, sticky='w', pady=5)

tk.Label(frame, text="Evaluation Period", anchor='w', bg="white").grid(row=2, column=0, sticky='w', pady=5)
eval_period_var = tk.StringVar()
eval_dropdown = ttk.Combobox(frame, textvariable=eval_period_var, width=27, state="readonly")
eval_dropdown['values'] = _display_values
eval_dropdown.grid(row=2, column=1, pady=5, columnspan=2)
eval_dropdown.bind("<<ComboboxSelected>>", on_period_select)

tk.Label(frame, text="Overall Student Rating", anchor='w', bg="white").grid(row=3, column=0, sticky='w', pady=5)
overall_var = tk.StringVar(value=str(overall_rating))
tk.Entry(frame, textvariable=overall_var, width=30, state="readonly").grid(row=3, column=1, pady=5, columnspan=2)

tk.Button(frame, text="View Student Feedbacks", command=open_feedback_window, bg="#0b5394", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

# New Metrics
tk.Label(frame, text="Student Feedback", anchor='w', bg="white").grid(row=5, column=0, sticky='w', pady=5)
stu_var = tk.StringVar()
tk.Entry(frame, textvariable=stu_var, width=30, state="readonly").grid(row=5, column=1, pady=5)

tk.Label(frame, text="Task Efficiency", anchor='w', bg="white").grid(row=6, column=0, sticky='w', pady=5)
task_var = tk.StringVar()
tk.Entry(frame, textvariable=task_var, width=30, state="readonly").grid(row=6, column=1, pady=5)

tk.Label(frame, text="Engagement Level", anchor='w', bg="white").grid(row=7, column=0, sticky='w', pady=5)
engage_var = tk.StringVar()
tk.Entry(frame, textvariable=engage_var, width=30, state="readonly").grid(row=7, column=1, pady=5)

tk.Label(frame, text="Use of Examples", anchor='w', bg="white").grid(row=8, column=0, sticky='w', pady=5)
examples_var = tk.StringVar()
tk.Entry(frame, textvariable=examples_var, width=30, state="readonly").grid(row=8, column=1, pady=5)

tk.Label(frame, text="Adaptability", anchor='w', bg="white").grid(row=9, column=0, sticky='w', pady=5)
adapt_var = tk.StringVar()
tk.Entry(frame, textvariable=adapt_var, width=30, state="readonly").grid(row=9, column=1, pady=5)

tk.Label(frame, text="After Class Responsiveness", anchor='w', bg="white").grid(row=10, column=0, sticky='w', pady=5)
resp_var = tk.StringVar()
tk.Entry(frame, textvariable=resp_var, width=30, state="readonly").grid(row=10, column=1, pady=5)

tk.Label(frame, text="Confidence Boost", anchor='w', bg="white").grid(row=11, column=0, sticky='w', pady=5)
conf_var = tk.StringVar()
tk.Entry(frame, textvariable=conf_var, width=30, state="readonly").grid(row=11, column=1, pady=5)

tk.Label(frame, text="Final Score", anchor='w', bg="white").grid(row=12, column=0, sticky='w', pady=5)
final_var = tk.StringVar()
tk.Entry(frame, textvariable=final_var, width=30, state="readonly").grid(row=12, column=1, pady=5)

tk.Button(frame, text="Log out", command=root.destroy, bg="#c0392b", width=15).grid(row=13, column=0, columnspan=2, pady=15)

root.mainloop()
