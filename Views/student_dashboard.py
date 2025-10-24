import subprocess
import os
import sys
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml
from models import get_pending_tutors, get_completed_count, submit_rating



class StudentDashboard:
    def __init__(self, root, student_id):
        self.root = root
        self.student_id = student_id
        self.root.title("Student Dashboard")
        self.root.geometry("600x500")
        
        # Dashboard heading
        self.heading_label = tk.Label(root, text="Student Dashboard", font=("Arial", 20, "bold"))
        self.heading_label.pack(pady=10)
        
        # Info labels
        self.name_label = tk.Label(root, text="", font=("Arial", 14))
        self.name_label.pack()
        
        self.pending_label = tk.Label(root, text="", font=("Arial", 12))
        self.pending_label.pack()
        
        self.completed_label = tk.Label(root, text="", font=("Arial", 12))
        self.completed_label.pack()
        
        # Tutor listbox
        self.tutor_listbox = tk.Listbox(root, width=40, height=10, font=("Arial", 12))
        self.tutor_listbox.pack(pady=10)
        
        # Rating entry
        self.rating_label = tk.Label(root, text="Enter Rating (1-5):", font=("Arial", 12))
        self.rating_label.pack()
        self.rating_entry = tk.Entry(root, font=("Arial", 12))
        self.rating_entry.pack(pady=5)
        
        # Comment entry
        self.comment_label = tk.Label(root, text="Enter Comment:", font=("Arial", 12))
        self.comment_label.pack()
        self.comment_entry = tk.Entry(root, font=("Arial", 12), width=50)
        self.comment_entry.pack(pady=5)
        
        # Submit button
        self.submit_button = tk.Button(root, text="Submit Rating", font=("Arial", 12, "bold"), bg="green", fg="white", command=self.submit_rating)
        self.submit_button.pack(pady=10)
        
        # Load initial data
        self.refresh_dashboard()

    def refresh_dashboard(self):
         """Load student info, pending tutors, and counts."""
         student_info, pending_count, completed_count = ml.get_student_dashboard_data(self.student_id)
         self.name_label.config(text=f"Welcome, {student_info['name']}")
         self.pending_label.config(text=f"Pending Tutors: {pending_count}")
         self.completed_label.config(text=f"Completed Ratings: {completed_count}")
        
         self.tutor_listbox.delete(0, tk.END)
         self.pending_tutors = get_pending_tutors(self.student_id)  # Get updated tutor list
        
         if not self.pending_tutors:
            self.tutor_listbox.insert(tk.END, "🎉 No tutors left to rate this month!")
         else:
            for tutor in self.pending_tutors:
                self.tutor_listbox.insert(tk.END, tutor["name"])

    def rate_tutor(self):
        selection = self.tutor_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a tutor.")
            return

        selected_tutor = self.tutor_listbox.get(selection[0])
        if "No tutors left" in selected_tutor:
            return

        employee_id = selected_tutor.split(" - ")[0]

        try:
            rating = int(self.rating_entry.get())
            task_efficiency = int(self.task_eff_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Rating and Task Efficiency must be numbers.")
            return

        comment = self.comment_entry.get()

        submit_rating(self.student_id, employee_id, rating, comment, task_efficiency)
        messagebox.showinfo("Success", "Tutor rated successfully!")

        # Clear inputs
        self.rating_entry.delete(0, tk.END)
        self.task_eff_entry.delete(0, tk.END)
        self.comment_entry.delete(0, tk.END)

        # Refresh list and counters
        self.refresh_dashboard()

def launch_student_dashboard(student_id):
    def refresh_dashboard():
        root.destroy()
        launch_student_dashboard(student_id)

    data = ml.get_student_dashboard_data(student_id)
    if not data:
        print("Student not found or dashboard data incomplete.")
        return

    student_name = data["name"]
    course = data["course"]
    pending_count = data["pending_count"]
    completed_count = data["completed_count"]
    tutors = data["tutors"]

    root = tk.Tk()
    root.title("Student Dashboard - ProMetric")
    root.geometry("850x550")
    root.config(bg="black")

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "Dashboard_bg.jpeg")
    try:
        bg_img = Image.open(image_path)
        bg_img = bg_img.resize((850, 550), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Background image load error:", e)

    frame = tk.Frame(root, bg="white", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # back button to host
    try:
        ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
    except Exception:
        pass

    tk.Label(frame, text="Student Dashboard", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=4, pady=10)
    tk.Label(frame, text=f"Hey, {student_name}", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=5)
    tk.Label(frame, text=f"Student ID: {student_id}", bg="white").grid(row=2, column=0, sticky="w")
    tk.Label(frame, text=f"Course Program: {course}", bg="white").grid(row=3, column=0, sticky="w")
    tk.Label(frame, text="Academic Standing: Good", bg="white").grid(row=5, column=0, sticky="w")

    tk.Label(frame, text=f"Pending Ratings: {pending_count}", bg="white", font=("Arial", 11)).grid(row=2, column=2, sticky="w")
    tk.Label(frame, text=f"Completed Ratings: {completed_count}", bg="white", font=("Arial", 11)).grid(row=3, column=2, sticky="w")

    tk.Label(frame, text="Tutors Awaiting Feedback", font=("Arial", 11, "bold"), bg="white").grid(row=5, column=0, columnspan=4, pady=(20, 5), sticky="w")

    selected_tutor = tk.StringVar(value="")

    if tutors:
        for i, tutor in enumerate(tutors):
            rb = tk.Radiobutton(
                frame,
                text=tutor,
                variable=selected_tutor,
                value=tutor,
                bg="white"
            )
            rb.grid(row=6 + i, column=0, columnspan=3, sticky="w")

        def open_feedback_window():
            tutor_name = selected_tutor.get()
            if not tutor_name:
                messagebox.showwarning("No Selection", "Please select a tutor to rate.")
                return

            subprocess.call([
                sys.executable,
                os.path.join(os.path.dirname(__file__), "feedback.py"),
                tutor_name,
                str(student_id)
            ])
            refresh_dashboard()

        tk.Button(
            frame,
            text="Rate Selected Tutor",
            bg="#0b5394",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5,
            command=open_feedback_window
        ).grid(row=6 + len(tutors) + 1, column=0, columnspan=4, pady=20)
    else:
        tk.Label(
            frame,
            text="\U0001F389 You've rated all your tutors for this month! Check back later.",
            font=("Arial", 11, "italic"),
            fg="#2e8b57",
            bg="white"
        ).grid(row=6, column=0, columnspan=4, pady=15)

    tk.Button(
        frame,
        text="Exit",
        command=root.destroy,
        bg="#c0392b",
        fg="white",
        width=15,
    ).grid(row=7 + len(tutors) + 1, column=0, columnspan=4, pady=10)

    root.mainloop()
