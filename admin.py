import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from theme import apply_dark_theme

def open_admin_panel():
    window = tk.Toplevel()
    window.title("Admin Panel")
    window.geometry("700x550")

    apply_dark_theme(window)

    # --- DB Functions ---
    def fetch_products(search_text=""):
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        if search_text:
            cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_text + '%',))
        else:
            cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_product():
        name = name_entry.get()
        qty = quantity_entry.get()
        price = price_entry.get()

        if not name or not qty or not price:
            messagebox.showwarning("Missing", "Please fill all fields.")
            return

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, qty, price))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"{name} added!")
        clear_fields()
        load_products()

    def update_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a product to update.")
            return

        pid = tree.item(selected[0])['values'][0]
        name = name_entry.get()
        qty = quantity_entry.get()
        price = price_entry.get()

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?", (name, qty, price, pid))
        conn.commit()
        conn.close()
        messagebox.showinfo("Updated", f"Product ID {pid} updated.")
        clear_fields()
        load_products()

    def delete_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a product to delete.")
            return

        pid = tree.item(selected[0])['values'][0]
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", f"Product ID {pid} deleted.")
        clear_fields()
        load_products()

    def clear_fields():
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

    def load_products():
        for row in tree.get_children():
            tree.delete(row)
        for row in fetch_products(search_var.get()):
            tree.insert("", tk.END, values=row)

    def on_select(event):
        selected = tree.selection()
        if selected:
            data = tree.item(selected[0])['values']
            name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            name_entry.insert(0, data[1])
            quantity_entry.insert(0, data[2])
            price_entry.insert(0, data[3])

    def on_search_key(event):
        load_products()

    # --- UI Layout ---
    tk.Label(window, text="Admin Panel", font=("Arial", 16, "bold"), fg="white", bg="#2e2e2e").pack(pady=10)

    search_var = tk.StringVar()
    tk.Label(window, text="Search Product", bg="#2e2e2e", fg="white").pack()
    search_entry = tk.Entry(window, textvariable=search_var)
    search_entry.pack()
    search_entry.bind("<KeyRelease>", on_search_key)

    # --- Product Table ---
    columns = ("ID", "Name", "Quantity", "Price")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(pady=10, fill=tk.BOTH, expand=True)
    tree.bind("<<TreeviewSelect>>", on_select)

    # --- Form Fields ---
    form_frame = tk.Frame(window, bg="#2e2e2e")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Name", bg="#2e2e2e", fg="white").grid(row=0, column=0, sticky="e")
    name_entry = tk.Entry(form_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(form_frame, text="Quantity", bg="#2e2e2e", fg="white").grid(row=1, column=0, sticky="e")
    quantity_entry = tk.Entry(form_frame)
    quantity_entry.grid(row=1, column=1)

    tk.Label(form_frame, text="Price", bg="#2e2e2e", fg="white").grid(row=2, column=0, sticky="e")
    price_entry = tk.Entry(form_frame)
    price_entry.grid(row=2, column=1)

    # --- Buttons ---
    button_frame = tk.Frame(window, bg="#2e2e2e")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add", width=10, command=add_product).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Update", width=10, command=update_product).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Delete", width=10, command=delete_product).grid(row=0, column=2, padx=5)

    load_products()
