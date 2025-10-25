import tkinter as tk
from tkinter import messagebox
import os, sys
from PIL import Image, ImageTk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml

root = tk.Tk()
root.title("Suggest an Improvement")
root.geometry("700x560")
root.config(bg="black")

# back button to host
try:
    ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
except Exception:
    pass

try:
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "login screen background.png")
    bg_img = Image.open(image_path)
    bg_img = bg_img.resize((700, 600), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo
except Exception as e:
    print("Background image could not be loaded:", e)

# Positioning variables
start_y = 230
center_x = 350
entry_width = 180
vertical_offset = 30
purple_color = "#3E4AB8"

# Header
tk.Label(root, text="We value your suggestions!", font=("Arial", 14, "bold"),
         bg="#000000", fg="white").place(x=center_x - 130, y=start_y)

# Your Name Label + Entry inside purple Frame
tk.Label(root, text="Your Name:", bg="#000000", fg="white").place(x=center_x - entry_width - 20, y=start_y + vertical_offset)
name_frame = tk.Frame(root, bg=purple_color, bd=1)
name_frame.place(x=center_x - entry_width - 20, y=start_y + vertical_offset + 25)
name_var = tk.StringVar()
tk.Entry(name_frame, textvariable=name_var, width=25, bg="#1c1c1c", fg="white",
         insertbackground="white", relief="flat", font=("Arial", 10)).pack(padx=1, pady=1)

# Your Email Label + Entry inside purple Frame
tk.Label(root, text="Your Email:", bg="#000000", fg="white").place(x=center_x + 20, y=start_y + vertical_offset)
email_frame = tk.Frame(root, bg=purple_color, bd=1)
email_frame.place(x=center_x + 20, y=start_y + vertical_offset + 25)
email_var = tk.StringVar()
tk.Entry(email_frame, textvariable=email_var, width=25, bg="#1c1c1c", fg="white",
         insertbackground="white", relief="flat", font=("Arial", 10)).pack(padx=1, pady=1)

# Suggestion Label and Text Box with Purple Border
tk.Label(root, text="Your Suggestion:", bg="#000000", fg="white").place(x=center_x - 70, y=start_y + 105)
text_frame = tk.Frame(root, bg=purple_color, bd=1)
text_frame.place(x=center_x - 161, y=start_y + 130)
message_box = tk.Text(
    text_frame,
    height=6,
    width=45,
    wrap="word",
    relief="flat",
    bg="#1c1c1c",
    fg="white",
    insertbackground="white",
    font=("Arial", 10)
)
message_box.pack(padx=1, pady=1)

def submit():
    name = name_var.get().strip()
    email = email_var.get().strip()
    message = message_box.get("1.0", tk.END).strip()

    if not name or not email or not message:
        messagebox.showerror("Error", "All fields are required.")
        return

    ml.save_improvement_suggestion(name, email, message)
    messagebox.showinfo("Thank you", "Your suggestion has been submitted.")
    root.destroy()

tk.Button(root, text="Submit", bg="#0b5394", fg="white", command=submit).place(x=center_x - 40, y=start_y + 270)

root.mainloop()