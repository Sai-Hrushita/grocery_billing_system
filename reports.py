import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from theme import apply_dark_theme


def open_reports_window():
    window = tk.Toplevel()
    window.title("Sales Reports")
    window.geometry("800x500")

    # Search by Date
    tk.Label(window, text="Search by Date (YYYY-MM-DD):").pack(pady=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(window, textvariable=search_var, width=30)
    search_entry.pack()

    # Sales Table
    columns = ("Bill ID", "Customer", "Product", "Qty", "Total", "Date")
    tree = ttk.Treeview(window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def fetch_sales(date_filter=""):
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        if date_filter:
            cursor.execute("SELECT bill_id, customer_name, product_name, quantity, total_price, date FROM sales WHERE date LIKE ?", (date_filter + "%",))
        else:
            cursor.execute("SELECT bill_id, customer_name, product_name, quantity, total_price, date FROM sales")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        sales = fetch_sales(search_var.get())
        for sale in sales:
            tree.insert("", tk.END, values=sale)

    def on_search(event):
        load_data()

    def export_to_csv():
        sales = fetch_sales(search_var.get())
        if not sales:
            messagebox.showinfo("No Data", "No sales data to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(sales)

        messagebox.showinfo("Exported", f"Sales data exported to:\n{file_path}")

    # Buttons
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Refresh", width=15, command=load_data).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Export to CSV", width=15, command=export_to_csv).grid(row=0, column=1, padx=10)

    search_entry.bind("<KeyRelease>", on_search)

    load_data()
