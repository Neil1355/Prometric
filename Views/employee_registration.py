from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
import sys, os
import datetime

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

def on_role_change(event=None):
    role = role_var.get()
    if role.lower() == "manager":
        tutored_subject_entry.delete(0, tk.END)
        tutored_subject_entry.config(state="disabled")
    else:
        tutored_subject_entry.config(state="normal")

def register():
    email = email_var.get().strip()
    name = name_var.get().strip()
    tutored_subject = tutored_subject_var.get().strip()
    dept = dept_var.get().strip()
    password = pass_var.get().strip()
    confirm_password = conf_pass_var.get().strip()
    role = role_var.get().strip()

    date_joined = datetime.date.today().strftime("%Y-%m-%d")

    if role.lower() == "manager":
        required_fields = [email, name, dept, password, confirm_password, role]
    else:
        required_fields = [email, name, tutored_subject, dept, password, confirm_password, role]

    if not all(required_fields):
        messagebox.showwarning("Missing Fields", "Please fill all fields.")
        return

    if password != confirm_password:
        messagebox.showerror("Password Mismatch", "Passwords do not match.")
        return

    data = {
        "email": email,
        "full_name": name,
        "tutored_subject": tutored_subject,
        "center": dept,
        "date_joined": date_joined,
        "password": password,
        "role": role,
        "security_question": sec_question_var.get() or None,
        "security_answer": sec_answer_var.get() or None
    }

    if role.lower() == "manager":
        manager_id = ml.register_manager(data)
        if manager_id:
            messagebox.showinfo("Success", f"{role} Registered Successfully!")
            clear_fields()
            ml.launch_manager_dashboard(root)
        else:
            messagebox.showerror("Database Error", "Manager registration failed. Check console for details.")
    else:
        employee_id = ml.register_employee(data)
        if employee_id:
            session_id = ml.create_review_session(employee_id)
            if session_id is None:
                messagebox.showerror("Database Error", "Failed creating review session.")
                return
            ml.insert_default_ratings(employee_id, session_id, data["role"])
            messagebox.showinfo("Success", f"{role} Registered Successfully!")
            clear_fields()
            ml.launch_employee_login(root)
        else:
            messagebox.showerror("Database Error", "Registration failed. Check console for details.")

def clear_fields():
    email_var.set("")
    name_var.set("")
    tutored_subject_var.set("")
    dept_var.set("")
    pass_var.set("")
    conf_pass_var.set("")
    role_var.set("Tutor")
    tutored_subject_entry.config(state="normal")

root = tk.Tk()
root.title("Employer Registration - ProMetric")
root.geometry("620x720")
root.config(bg="black")

base_dir = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "login_bg.jpg")
bg_img = Image.open(image_path)
bg_img = bg_img.resize((620, 720), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

email_var = tk.StringVar()
name_var = tk.StringVar()
tutored_subject_var = tk.StringVar()
dept_var = tk.StringVar()
pass_var = tk.StringVar()
conf_pass_var = tk.StringVar()
role_var = tk.StringVar(value="Tutor")
sec_question_var = tk.StringVar()
sec_answer_var = tk.StringVar()

frame = tk.Frame(root, bg="white", padx=20, pady=20, width=540, height=620)
frame.place(relx=0.5, rely=0.5, anchor='center')
frame.pack_propagate(False)

# back button to host
try:
    ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
except Exception:
    pass

tk.Label(frame, text="Employer Registration", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

fields = [
    ("Email Address", email_var),
    ("Full Name", name_var),
    ("center", dept_var),
    ("Password", pass_var),
    ("Confirm Password", conf_pass_var)
]

for i, (label_text, var) in enumerate(fields, start=1):
    tk.Label(frame, text=label_text, anchor='w', bg="white").grid(row=i, column=0, sticky='w', pady=5)
    show_char = "*" if "Password" in label_text else ""
    entry = tk.Entry(frame, textvariable=var, width=40, show=show_char)
    entry.grid(row=i, column=1, pady=5)

tk.Label(frame, text="Tutored Subject", anchor='w', bg="white").grid(row=6, column=0, sticky='w', pady=5)
tutored_subject_entry = tk.Entry(frame, textvariable=tutored_subject_var, width=30)
tutored_subject_entry.grid(row=6, column=1, pady=5)

# Security question fields (rows 7-8)
tk.Label(frame, text="Security Question", anchor='w', bg="white").grid(row=7, column=0, sticky='w', pady=5)
sec_q_cb = ttk.Combobox(
    frame,
    textvariable=sec_question_var,
    values=[
            "Select one",
            "What's your Mother's maiden name?",
            "What's your Best friend's name?",
            "What's your Place of birth?",
    ],
    state='readonly',
    width=36
)
sec_q_cb.current(0)
sec_q_cb.grid(row=7, column=1, pady=5)

tk.Label(frame, text="Security Answer", anchor='w', bg="white").grid(row=8, column=0, sticky='w', pady=5)
tk.Entry(frame, textvariable=sec_answer_var, show='', width=40).grid(row=8, column=1, pady=5)

# Role selector moved to row 9
tk.Label(frame, text="Role", anchor='w', bg="white").grid(row=9, column=0, sticky='w', pady=5)
role_dropdown = ttk.Combobox(frame, textvariable=role_var, values=["Tutor", "Manager"], width=27, state="readonly")
role_dropdown.grid(row=9, column=1, pady=5)
role_dropdown.set("Tutor")
role_dropdown.bind("<<ComboboxSelected>>", on_role_change)

# place buttons below the last field
next_row = 11
tk.Button(frame, text="Register", command=register, bg="#0b5394", fg="white", width=12).grid(row=next_row, column=0, pady=18)
tk.Button(frame, text="Clear", command=clear_fields, width=12).grid(row=next_row, column=1)

login_label = tk.Label(frame, text="Already Registered? Login", fg="blue", bg="white", cursor="hand2")
login_label.grid(row=next_row + 1, column=0, columnspan=2, pady=(5, 0))
login_label.bind("<Button-1>", lambda e: ml.launch_employee_login(root))

root.mainloop()
