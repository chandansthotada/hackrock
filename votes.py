import tkinter as tk
from tkinter import messagebox
from faces import register_user, verify_user, cast_vote, capture_face, match_face
import cv2

root = tk.Tk()
root.title("Smart Voting System")
root.geometry("400x400")
root.configure(bg="lightblue")

tk.Label(root, text="Smart Voting System", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=30)

# ===================== REGISTER =========================
def open_register_window():
    reg_win = tk.Toplevel(root)
    reg_win.title("Register")
    reg_win.geometry("300x300")

    tk.Label(reg_win, text="Aadhaar").pack(pady=5)
    aadhaar_entry = tk.Entry(reg_win)
    aadhaar_entry.pack()

    tk.Label(reg_win, text="Password").pack(pady=5)
    password_entry = tk.Entry(reg_win, show="*")
    password_entry.pack()

    def register():
        aadhaar = aadhaar_entry.get()
        password = password_entry.get()

        if not aadhaar or not password:
            messagebox.showerror("Error", "Enter all fields")
            return

        register_user(aadhaar, password)
        capture_face(aadhaar)
        messagebox.showinfo("Success", "Registered successfully!")
        reg_win.destroy()

    tk.Button(reg_win, text="Submit", command=register, bg="green", fg="white").pack(pady=20)

# ===================== VERIFY =========================
def open_verify_window():
    ver_win = tk.Toplevel(root)
    ver_win.title("Verify")
    ver_win.geometry("300x300")

    tk.Label(ver_win, text="Aadhaar").pack(pady=5)
    aadhaar_entry = tk.Entry(ver_win)
    aadhaar_entry.pack()

    tk.Label(ver_win, text="Password").pack(pady=5)
    password_entry = tk.Entry(ver_win, show="*")
    password_entry.pack()

    def verify():
        aadhaar = aadhaar_entry.get()
        password = password_entry.get()

        if not verify_user(aadhaar, password):
            messagebox.showerror("Error", "Invalid credentials")
            return

        if match_face(aadhaar):
            messagebox.showinfo("Verified", "Face and credentials matched.")
            ver_win.destroy()
        else:
            messagebox.showerror("Error", "Face does not match.")

    tk.Button(ver_win, text="Verify", command=verify, bg="blue", fg="white").pack(pady=20)

# ===================== VOTE =========================
def open_vote_window():
    vote_win = tk.Toplevel(root)
    vote_win.title("Vote")
    vote_win.geometry("300x300")

    tk.Label(vote_win, text="Aadhaar").pack(pady=5)
    aadhaar_entry = tk.Entry(vote_win)
    aadhaar_entry.pack()

    def vote(party):
        aadhaar = aadhaar_entry.get()
        if not aadhaar:
            messagebox.showerror("Error", "Enter Aadhaar")
            return
        cast_vote(aadhaar, party)
        messagebox.showinfo("Success", f"Voted for {party}")
        vote_win.destroy()

    tk.Button(vote_win, text="Vote Party A", command=lambda: vote("Party A"), bg="orange", fg="white").pack(pady=5)
    tk.Button(vote_win, text="Vote Party B", command=lambda: vote("Party B"), bg="orange", fg="white").pack(pady=5)

# ===================== BUTTONS =========================
tk.Button(root, text="Register", width=20, bg="green", fg="white", font=("Arial", 12), command=open_register_window).pack(pady=10)
tk.Button(root, text="Verify", width=20, bg="blue", fg="white", font=("Arial", 12), command=open_verify_window).pack(pady=10)
tk.Button(root, text="Vote", width=20, bg="orange", fg="white", font=("Arial", 12), command=open_vote_window).pack(pady=10)
tk.Button(root, text="Exit", width=20, bg="red", fg="white", font=("Arial", 12), command=root.quit).pack(pady=10)

root.mainloop()
