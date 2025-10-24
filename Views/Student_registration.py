import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import sys
import os

# Add model path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

def register():
    full_name = full_name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    course = course_var.get()
    center = dept_var.get()
    password = pass_var.get()
    confirm_password = conf_pass_var.get()

    if not all([full_name, email, phone, course, center, password, confirm_password]):
        messagebox.showwarning("Missing Fields", "Please fill all fields.")
    elif password != confirm_password:
        messagebox.showerror("Password Mismatch", "Passwords do not match.")
    else:
        data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "course": course.strip(),  # comma-separated subjects
            "center": center,
            "password": password,
            "security_question": sec_question_var.get() or None,
            "security_answer": sec_answer_var.get() or None
        }
        if ml.register_student(data):
            messagebox.showinfo("Success", "Student Registered Successfully!")
            clear_fields()
            root.destroy()
            subprocess.run(["python", "C:\\Users\\neilb\\OneDrive\\Desktop\\neil barot\\programs\\Python\\ProMetric\\Source Code\\Views\\student_login.py"])
        else:
            messagebox.showerror("Error", "Registration Failed!")

def clear_fields():
    full_name_var.set("")
    email_var.set("")
    phone_var.set("")
    course_var.set("")
    dept_var.set("")
    pass_var.set("")
    conf_pass_var.set("")

# GUI setup
root = tk.Tk()
root.title("Student Registration - ProMetric")
root.geometry("620x720")
root.config(bg="black")

# Background image
base_dir = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "login_bg.jpg")
bg_img = Image.open(image_path)
bg_img = bg_img.resize((620, 720), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Variables
full_name_var = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()
course_var = tk.StringVar()
dept_var = tk.StringVar()
pass_var = tk.StringVar()
conf_pass_var = tk.StringVar()
sec_question_var = tk.StringVar()
sec_answer_var = tk.StringVar()

# Frame
frame = tk.Frame(root, bg="white", padx=20, pady=20, width=540, height=620)
frame.place(relx=0.5, rely=0.5, anchor='center')
# keep the white box size fixed so controls don't overlap
frame.pack_propagate(False)

# back button to host
try:
    ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
except Exception:
    pass

tk.Label(frame, text="Student Registration", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

labels = [
    "Full Name:", "Email Address:", "Phone Number:",
    "Course (comma-separated):", "center:",
    "Password:", "Confirm Password:",
    "Security Question:", "Security Answer:"
]
vars = [full_name_var, email_var, phone_var, course_var, dept_var, pass_var, conf_pass_var, sec_question_var, sec_answer_var]

for i, (label, var) in enumerate(zip(labels, vars), start=1):
    tk.Label(frame, text=label, anchor='w', bg="white").grid(row=i, column=0, sticky='w', pady=5)
    # security question uses a combobox with common questions
    if label == "Security Question:":
        cb = ttk.Combobox(
            frame,
            textvariable=var,
            values=[
                "Select one",
                "What's your Mother's maiden name?",
                "What's your Best friend's name?",
                "What's your Place of birth?",
            ],
            state='readonly',
            width=36
        )
        cb.current(0)
        cb.grid(row=i, column=1, pady=5)
    else:
        # only mask password fields; security answer should be visible
        show_char = "*" if "Password" in label else ""
        entry = tk.Entry(frame, textvariable=var, width=40, show=show_char)
        entry.grid(row=i, column=1, pady=5)

# place buttons below the last field so they never overlap
next_row = len(labels) + 1
tk.Button(frame, text="Register", command=register, bg="#0b5394", fg="white", width=12).grid(row=next_row, column=0, pady=18)
tk.Button(frame, text="Clear", command=clear_fields, width=12).grid(row=next_row, column=1, pady=18)

login_label = tk.Label(frame, text="Already Registered? Login", fg="blue", bg="white", cursor="hand2")
login_label.grid(row=next_row + 1, column=0, columnspan=2, pady=(5, 0))
login_label.bind("<Button-1>", lambda e: ml.launch_student_login(root))
root.mainloop()
