import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# make importing this module safe (don't create a UI at import time)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Model')))
import models as ml


def launch_forgot_password():
    """Create and run the forgot-password UI. This function is safe to import and
    can be used when the module is executed as a stand-alone script.
    """
    root = tk.Tk()
    root.title("Forgot Password - ProMetric")
    root.geometry("500x400")
    root.config(bg="white")

    # small header
    try:
        ml.make_back_button(root, ml.launch_host, text='\u2190 Back')
    except Exception:
        pass

    frame = tk.Frame(root, bg="white", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(frame, text="Verify your identity", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

    # user type
    user_type_var = tk.StringVar(value="student")
    ttk.Label(frame, text="Account Type:").pack(anchor='w')
    ttk.Combobox(frame, textvariable=user_type_var, values=["student", "employee", "manager"], state='readonly').pack(fill='x')

    # inputs
    first_var = tk.StringVar()
    last_var = tk.StringVar()
    email_var = tk.StringVar()

    ttk.Label(frame, text="First name:").pack(anchor='w', pady=(8,0))
    tk.Entry(frame, textvariable=first_var).pack(fill='x')

    ttk.Label(frame, text="Last name:").pack(anchor='w', pady=(8,0))
    tk.Entry(frame, textvariable=last_var).pack(fill='x')

    ttk.Label(frame, text="Email:").pack(anchor='w', pady=(8,0))
    tk.Entry(frame, textvariable=email_var).pack(fill='x')


    def verify():
        first = first_var.get().strip()
        last = last_var.get().strip()
        email = email_var.get().strip()
        utype = user_type_var.get().strip()
        if not first or not last or not email:
            messagebox.showwarning("Missing fields", "Please enter first name, last name and email.")
            return

        res = ml.verify_user_by_name_email(utype, first, last, email)
        if not res:
            messagebox.showerror("Not found", "No matching user found. Please check the details.")
            return

        # backward-compatible: models.verify_user_by_name_email may return (uid, table)
        # or the newer (uid, table, security_question)
        if isinstance(res, (list, tuple)) and len(res) == 3:
            uid, table, question = res
        else:
            uid, table = res
            question = None

        # If a security question exists, ask it; otherwise ask user to contact admin
        if question:
            show_question_screen(root, frame, utype, uid, question)
        else:
            messagebox.showinfo("No security question", "This account does not have a security question set. Please login and set one, or contact your administrator for a password reset.")


    def show_reset_screen(root, frame, utype, uid):
        for w in frame.winfo_children():
            w.destroy()

        tk.Label(frame, text="Set a new password", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

        new_var = tk.StringVar()
        conf_var = tk.StringVar()

        ttk.Label(frame, text="New password:").pack(anchor='w', pady=(8,0))
        tk.Entry(frame, textvariable=new_var, show='*').pack(fill='x')

        ttk.Label(frame, text="Confirm password:").pack(anchor='w', pady=(8,0))
        tk.Entry(frame, textvariable=conf_var, show='*').pack(fill='x')

        import threading

        set_btn = tk.Button(frame, text="Set Password", bg="#0b5394", fg='white')
        set_btn.pack(pady=15)

        def do_update():
            p1 = new_var.get()
            p2 = conf_var.get()
            if not p1 or not p2:
                messagebox.showwarning("Missing", "Please enter and confirm your new password.")
                return
            if p1 != p2:
                messagebox.showerror("Mismatch", "Passwords do not match.")
                return

            # disable button while running
            set_btn.config(state='disabled', text='Updating...')

            def _worker():
                try:
                    ok = ml.update_password(utype, uid, p1)
                except Exception as e:
                    ok = False
                    err = str(e)
                else:
                    err = None

                def _finish():
                    set_btn.config(state='normal', text='Set Password')
                    if ok:
                        messagebox.showinfo("Success", "Password updated. You can now login.")
                        try:
                            root.destroy()
                        except Exception:
                            pass
                    else:
                        msg = "Failed to update password. Check console for details."
                        if err:
                            msg += f"\nError: {err}"
                        messagebox.showerror("Error", msg)

                # schedule finish on main thread
                root.after(10, _finish)

            t = threading.Thread(target=_worker, daemon=True)
            t.start()

        set_btn.config(command=do_update)


    def show_question_screen(root, frame, utype, uid, question):
        # Clear frame and show the stored security question
        for w in frame.winfo_children():
            w.destroy()

        tk.Label(frame, text="Answer your security question", font=("Arial", 14, "bold"), bg="white").pack(pady=5)
        tk.Label(frame, text=question or "(no question)", bg="white", wraplength=420, justify='left').pack(pady=(6, 12))

        ans_var = tk.StringVar()
        ttk.Label(frame, text="Your answer:").pack(anchor='w')
        tk.Entry(frame, textvariable=ans_var, show='*').pack(fill='x')

        import threading

        def do_verify_answer():
            ans = ans_var.get().strip()
            if not ans:
                messagebox.showwarning("Missing", "Please enter your answer to the security question.")
                return

            # verify in background to avoid UI freeze
            def _worker():
                try:
                    ok = ml.verify_security_answer(utype, uid, ans)
                except Exception as e:
                    ok = False
                    err = str(e)
                else:
                    err = None

                def _finish():
                    if ok:
                        show_reset_screen(root, frame, utype, uid)
                    else:
                        msg = "Security answer incorrect."
                        if err:
                            msg += f"\nError: {err}"
                        messagebox.showerror("Verification failed", msg)

                root.after(10, _finish)

            t = threading.Thread(target=_worker, daemon=True)
            t.start()

        tk.Button(frame, text="Verify Answer", bg="#0b5394", fg='white', command=do_verify_answer).pack(pady=12)


    # verify button
    tk.Button(frame, text="Verify", bg="#0b5394", fg='white', command=verify).pack(pady=12)

    root.mainloop()


if __name__ == '__main__':
    launch_forgot_password()
