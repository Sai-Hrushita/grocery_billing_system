import tkinter as tk
from theme import apply_dark_theme
import billing
import admin
import reports
import dashboard

root = tk.Tk()
root.title("Grocery Store Billing System")
root.geometry("400x500")

apply_dark_theme(root) 

tk.Label(root, text="Grocery Store App", font=("Arial", 16, "bold"), fg="white", bg="#2e2e2e").pack(pady=20)

tk.Button(root, text="Billing System", width=30, command=billing.open_billing_window).pack(pady=10)
tk.Button(root, text="Admin Panel", width=30, command=admin.open_admin_panel).pack(pady=10)
tk.Button(root, text="Reports & Sales", width=30, command=reports.open_reports_window).pack(pady=10)
tk.Button(root, text="Dashboard", width=30, command=dashboard.open_dashboard).pack(pady=10)

# Optional: Quit button
tk.Button(root, text="Exit", width=30, command=root.destroy, fg="white", bg="#6c2e2e").pack(pady=30)

root.mainloop()
