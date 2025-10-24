import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

def login():
    manager_id = manager_id_var.get()
    password = pass_var.get()

    if not manager_id or not password:
        messagebox.showwarning("Missing Fields", "Please enter Manager ID and Password.")
    else:
        ok = ml.login_manager(manager_id, password)
        if ok:
            # check security fields by fetching from DB
            try:
                # manager_id may be email or id depending on table; try to use as id
                internal_id = ml.get_manager_details(manager_id)
            except Exception:
                internal_id = manager_id

            # get_security_fields expects numeric id; try both approaches
            try:
                q, h = ml.get_security_fields('manager', internal_id)
            except Exception:
                q, h = (None, None)

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
                    ok2 = ml.set_security_answer('manager', internal_id, q, ans)
                    if not ok2:
                        messagebox.showwarning('Warning', 'Failed to save security answer. You can set it later.')

            messagebox.showinfo("Login Success", f"Welcome, Manager!")
            root.destroy()  # Dispose the window
            subprocess.run(["python", "C:\\Users\\neilb\\OneDrive\\Desktop\\neil barot\\programs\\Python\\ProMetric\\Source Code\\Views\\manager_dashboard.py" , str(manager_id)])
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

def forgot_password():
    try:
        ml.launch_forgot_password(root)
    except Exception:
        messagebox.showinfo("Forgot Password", "Contact Admin or HR for password reset.")

root = tk.Tk()
root.title("Manager Login - ProMetric")
root.geometry("500x400")
root.config(bg="black")

base_dir = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "login_bg.jpg")
bg_img = Image.open(image_path)
bg_img = bg_img.resize((500, 650), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

manager_id_var = tk.StringVar()
pass_var = tk.StringVar()

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

# back button to host
try:
    ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
except Exception:
    pass

tk.Label(frame, text="Manager Login", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame, text="Email ID:", anchor='w', bg="white").grid(row=1, column=0, sticky='w', pady=5)
tk.Entry(frame, textvariable=manager_id_var, width=30).grid(row=1, column=1, pady=5)

tk.Label(frame, text="Password:", anchor='w', bg="white").grid(row=2, column=0, sticky='w', pady=5)
tk.Entry(frame, textvariable=pass_var, show="*", width=30).grid(row=2, column=1, pady=5)

tk.Button(frame, text="Log in", command=login, bg="#0b5394", fg="white", width=25).grid(row=3, column=0, columnspan=2, pady=15)

tk.Label(frame, text="Forgot Password?", fg="blue", bg="white", cursor="hand2").grid(row=4, column=0, columnspan=2)
frame.grid_slaves(row=4, column=0)[0].bind("<Button-1>", lambda e: forgot_password())

root.mainloop()
