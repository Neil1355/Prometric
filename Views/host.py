import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

root = tk.Tk()
root.title("Welcome to ProMetric")
root.geometry("700x600")
root.config(bg="black")

# bg image
try:
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "Dashboard_bg.jpeg")
    bg_img = Image.open(image_path)
    bg_img = bg_img.resize((900, 600), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo
except Exception as e:
    print("bg load error:", e)

# main frame
frame = tk.Frame(root, bg="white", padx=30, pady=30, bd=2, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor='center')

# title
tk.Label(frame, text="ProMetric", font=("Arial", 28, "bold"), bg="white", fg="#0b5394").pack(pady=(10, 5))

# tagline
tk.Label(frame, text="Empowering excellence in tutoring\nthrough insights and feedback.", font=("Arial", 12), bg="white", justify="center").pack(pady=(0, 25))

# buttons
btn_frame = tk.Frame(frame, bg="white")
btn_frame.pack()

buttons = [
    ("Student Registration", lambda: ml.launch_student_registration(root)),
    ("Student Login", lambda: ml.launch_student_login(root)),
    ("Employee Registration", lambda: ml.launch_employee_registration(root)),
    ("Employee Login", lambda: ml.launch_employee_login(root)),
    ("Manager Login", lambda: ml.launch_manager_login(root)),
    ("Suggest Improvement", lambda: ml.launch_suggest_improvement(root)),
]

btn_w, btn_h = 22, 2
for i, (text, cmd) in enumerate(buttons):
    btn = tk.Button(btn_frame, text=text, width=btn_w, height=btn_h, bg="#0b5394", fg="white", font=("Arial", 11, "bold"), relief="raised", bd=2, activebackground="#073763", activeforeground="white", command=cmd)
    r = i // 2
    c = i % 2
    btn.grid(row=r, column=c, padx=10, pady=10)

exit_btn = tk.Button(btn_frame, text="Exit", width=btn_w * 2 + 5, height=btn_h, bg="#c00000", fg="white", font=("Arial", 11, "bold"), relief="raised", bd=2, activebackground="#7f0000", activeforeground="white", command=root.quit)
exit_btn.grid(row=3, column=0, columnspan=2, pady=(20,10))

# footer
tk.Label(root, text="Created by Neil Barot@xpertinfotech\n ProMetric©", font=("Arial", 10), bg="black", fg="white").pack(side="bottom", pady=10)

root.mainloop()
