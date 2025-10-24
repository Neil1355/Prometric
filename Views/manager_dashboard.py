import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

if len(sys.argv) > 1:
    manager_id = sys.argv[1]
else:
    manager_id = None

manager_name = ml.get_manager_details(manager_id) if manager_id else "Unknown"

total_employees = ml.get_total_employees()
total_students = ml.get_total_student()
leaderboard_data = ml.get_employee_leaderboard()

root = tk.Tk()
root.title("Manager Dashboard - ProMetric")
root.geometry("1000x550")
root.config(bg="black")

try:
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "Dashboard_bg.jpeg")
    bg_img = Image.open(image_path)
    bg_img = bg_img.resize((1000, 550), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo
except Exception as e:
    print("Background image could not be loaded:", e)

def open_feedback_window(parent_window):
    feedback_win = tk.Toplevel(parent_window)
    feedback_win.title("Feedback Provided by Students")
    feedback_win.geometry("800x500")
    feedback_win.config(bg="white")

    tk.Label(
        feedback_win,
        text="Feedback Provided by Students",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(pady=10)

    scroll_canvas = tk.Canvas(feedback_win, bg="white", borderwidth=0, highlightthickness=0)
    scroll_frame = tk.Frame(scroll_canvas, bg="white")

    vsb = tk.Scrollbar(feedback_win, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    scroll_canvas.pack(side="left", fill="both", expand=True)
    scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def on_frame_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    scroll_frame.bind("<Configure>", on_frame_configure)

    all_feedbacks = ml.get_all_employee_feedbacks()

    current_tutor = None
    for record in all_feedbacks:
        emp_id, name, subjects, rating, comment = record

        if current_tutor != name:
            current_tutor = name
            tk.Label(
                scroll_frame,
                text=f"{name} ({subjects})",
                font=("Arial", 12, "bold"),
                bg="white",
                anchor="w"
            ).pack(fill="x", padx=20, pady=(15, 5))

        if rating is not None:
            text = f"⭐ {rating}/10 - {comment}"
            tk.Label(
                scroll_frame,
                text=text,
                font=("Arial", 10),
                bg="white",
                anchor="w",
                wraplength=750,
                justify="left"
            ).pack(fill="x", padx=40, pady=2)
        else:
            tk.Label(
                scroll_frame,
                text="No feedbacks provided yet...",
                font=("Arial", 10, "italic"),
                bg="white",
                anchor="w"
            ).pack(fill="x", padx=40, pady=(0, 10))

    tk.Button(
        feedback_win,
        text="Close Feedback Window",
        command=feedback_win.destroy,
        bg="#c0392b",
        fg="white"
    ).pack(pady=10)

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

# back button to host
try:
    ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
except Exception:
    pass

tk.Label(frame, text="Manager Dashboard", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=4, pady=10)
tk.Label(frame, text=f"Hey, {manager_name}", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=(0, 10))

tk.Label(frame, text="Manager ID:", bg="white").grid(row=2, column=0, sticky="w")
tk.Label(frame, text=manager_id, bg="white").grid(row=2, column=1, sticky="w", padx=5)

tk.Label(frame, text="Total Employees:", bg="white").grid(row=3, column=0, sticky="w")
tk.Label(frame, text=total_employees, bg="white").grid(row=3, column=1, sticky="w", padx=5)

tk.Label(frame, text="Total Students:", bg="white").grid(row=4, column=0, sticky="w")
tk.Label(frame, text=total_students, bg="white").grid(row=4, column=1, sticky="w", padx=5)

tk.Button(
    frame,
    text="View All Feedback",
    command=lambda: open_feedback_window(root),
    bg="#0b5394",
    fg="white",
    width=20
).grid(row=5, column=0, columnspan=2, pady=20)

tk.Button(
    frame,
    text="Exit Dashboard",
    command=root.destroy,
    bg="#c0392b",
    fg="white",
    width=20
).grid(row=6, column=0, columnspan=2, pady=10)

columns = ("name", "avg_rating", "kpi")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=5)
tree.grid(row=2, column=2, columnspan=2, rowspan=4, padx=20)

tree.heading("name", text="Name")
tree.heading("avg_rating", text="Average Rating")
tree.heading("kpi", text="KPI Comparisons")

for item in tree.get_children():
    tree.delete(item)

for i, row in enumerate(leaderboard_data, start=1):
    name, avg_rating = row
    # display dash for unrated
    display_rating = '-' if avg_rating is None else avg_rating

    if avg_rating is None:
        kpi = ''
    else:
        try:
            v = float(avg_rating)
        except Exception:
            v = 0.0
        if v >= 8:
            kpi = "⭐"
        elif v >= 7:
            kpi = "👍"
        else:
            kpi = "⚠"

    tree.insert("", tk.END, values=(f"{i}. {name}", display_rating, kpi))

root.mainloop()
