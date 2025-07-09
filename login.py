import tkinter as tk
from tkinter import messagebox
import sqlite3
from theme import apply_dark_theme
import main  # Will call main_app(role) after login

def open_login_window():
    root = tk.Tk()
    root.title("Login - Grocery App")
    root.geometry("400x300")
    root.resizable(False, False)

    apply_dark_theme(root)

    tk.Label(root, text="Login", font=("Arial", 18, "bold"), bg="#2e2e2e", fg="white").pack(pady=20)

    frame = tk.Frame(root, bg="#2e2e2e")
    frame.pack()

    tk.Label(frame, text="Username:", bg="#2e2e2e", fg="white").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1, pady=10)

    tk.Label(frame, text="Password:", bg="#2e2e2e", fg="white").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(frame, show="*")
    password_entry.grid(row=1, column=1, pady=10)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()

        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == password:
            messagebox.showinfo("Login Success", f"Welcome, {username} ({result[1]})!")
            root.destroy()
            main.main_app(result[1])  # Pass role to main.py
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(root, text="Login", width=15, command=login).pack(pady=20)

    root.mainloop()
