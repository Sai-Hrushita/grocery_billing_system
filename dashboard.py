import sqlite3
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from theme import apply_dark_theme

def open_dashboard():
    root = Toplevel()
    root.title("📊 Sales Dashboard")
    root.geometry("1000x700")

    apply_dark_theme(root)

    Label(root, text="From:", font=("Arial", 12), bg="#2e2e2e", fg="white").pack()
    from_date = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, year=2025)
    from_date.pack(pady=5)

    Label(root, text="To:", font=("Arial", 12), bg="#2e2e2e", fg="white").pack()
    to_date = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, year=2025)
    to_date.pack(pady=5)

    Button(root, text="📊 Filter Dashboard", command=lambda: update_dashboard(from_date.get(), to_date.get())).pack(pady=10)

    global chart_frame, total_label

    chart_frame = Frame(root, bg="#2e2e2e")
    chart_frame.pack(pady=10)

    total_label = Label(root, text="💰 Total Revenue: ₹0.00", font=("Arial", 14, "bold"), bg="#2e2e2e", fg="white")
    total_label.pack(pady=10)

def update_dashboard(start_date, end_date):
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()

    try:
        # Convert to YYYY-MM-DD
        start = datetime.strptime(start_date, "%m/%d/%y").strftime("%Y-%m-%d")
        end = datetime.strptime(end_date, "%m/%d/%y").strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT product_name, SUM(quantity) as total_qty, SUM(total_price) as total_sales
            FROM sales
            WHERE date BETWEEN ? AND ?
            GROUP BY product_name
            ORDER BY total_qty DESC
            LIMIT 5
        """, (start, end))

        data = cursor.fetchall()

        product_names = [row[0] for row in data]
        quantities = [row[1] for row in data]
        total_revenue = sum(row[2] for row in data)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(product_names, quantities, color='skyblue')
        ax.set_title("Top 5 Best-Selling Products")
        ax.set_ylabel("Quantity Sold")
        ax.set_xlabel("Product")

        for widget in chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        total_label.config(text=f"💰 Total Revenue: ₹{total_revenue:.2f}")

    except Exception as e:
        print("Dashboard Error:", e)

    conn.close()
