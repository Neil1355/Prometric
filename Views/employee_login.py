import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

def login():
    email_id = emp_id_var.get()
    password = pass_var.get()

    if not email_id or not password:
        messagebox.showwarning("Missing Fields", "Please enter both Email ID and Password.")
    else:
        emp_id = ml.login_employee(email_id, password)
        if emp_id:
            # After successful login, check security fields and prompt if question exists but no answer hash
            # First get internal employee id (some login helpers return id differently)
            try:
                internal_id = ml.get_employee_id_by_email(email_id)
            except Exception:
                internal_id = None

            if internal_id:
                q, h = ml.get_security_fields('employee', internal_id)
                if q and not h:
                    ans = None
                    def on_submit():
                        nonlocal ans
                        ans = ans_var.get().strip()
                        dlg.destroy()

                    dlg = tk.Toplevel(root)
                    dlg.title('Set security answer')
                    tk.Label(dlg, text='Please answer your security question to secure your account:', wraplength=300).pack(padx=10, pady=6)
                    tk.Label(dlg, text=q, font=(None, 10, 'bold')).pack(padx=10, pady=(0,6))
                    ans_var = tk.StringVar()
                    tk.Entry(dlg, textvariable=ans_var, show='*', width=40).pack(padx=10, pady=6)
                    tk.Button(dlg, text='Set Answer', command=on_submit, bg='#0b5394', fg='white').pack(pady=8)
                    dlg.transient(root)
                    dlg.grab_set()
                    root.wait_window(dlg)

                    if ans:
                        ok2 = ml.set_security_answer('employee', internal_id, q, ans)
                        if not ok2:
                            messagebox.showwarning('Warning', 'Failed to save security answer. You can set it later.')

            messagebox.showinfo("Login Success", "Welcome!")
            try:
                root.destroy()
            except Exception:
                pass
            ml.launch_employee_dashboard(email_id)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")


def forgot_password():
    try:
        ml.launch_forgot_password(root)
    except Exception:
        messagebox.showinfo("Forgot Password", "Redirecting to password recovery...")

root = tk.Tk()
root.title("Employee Login - ProMetric")
root.geometry("500x400")
root.config(bg="black")

base_dir = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "login_bg.jpg")
bg_img = Image.open(image_path)
bg_img = bg_img.resize((500, 650), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

emp_id_var = tk.StringVar()
pass_var = tk.StringVar()

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

# back button to host
try:
    ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
except Exception:
    pass

tk.Label(frame, text="Employee Login", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame, text="Email ID:", anchor='w', bg="white").grid(row=1, column=0, sticky='w', pady=5)
tk.Entry(frame, textvariable=emp_id_var, width=30).grid(row=1, column=1, pady=5)

tk.Label(frame, text="Password:", anchor='w', bg="white").grid(row=2, column=0, sticky='w', pady=5)
tk.Entry(frame, textvariable=pass_var, show="*", width=30).grid(row=2, column=1, pady=5)

tk.Button(frame, text="Log in", command=login, bg="#0b5394", fg="white", width=25).grid(row=3, column=0, columnspan=2, pady=15)

tk.Label(frame, text="Forgot Password?", fg="blue", bg="white", cursor="hand2").grid(row=4, column=0, columnspan=2)
frame.grid_slaves(row=4, column=0)[0].bind("<Button-1>", lambda e: forgot_password())

root.mainloop()
