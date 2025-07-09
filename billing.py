import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import random
from pdf_generator import generate_bill_pdf
from database import update_inventory, save_to_sales
from theme import apply_dark_theme 

def get_all_products():
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products")
    products = [row[0] for row in cursor.fetchall()]
    conn.close()
    return products

def get_product_price(product_name):
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM products WHERE name = ?", (product_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def open_billing_window():
    window = tk.Toplevel()
    window.title("Billing System")
    window.geometry("400x650")

    apply_dark_theme(window)  # ✅ Apply Dark Theme here

    cart_items = []

    # Customer Info
    tk.Label(window, text="Customer Name").pack()
    customer_name_entry = tk.Entry(window)
    customer_name_entry.pack()

    tk.Label(window, text="Phone Number").pack()
    customer_phone_entry = tk.Entry(window)
    customer_phone_entry.pack()

    tk.Label(window, text="Email Address").pack()
    customer_email_entry = tk.Entry(window)
    customer_email_entry.pack()

    # Product Dropdown
    tk.Label(window, text="Select Product").pack()
    product_var = tk.StringVar()
    product_dropdown = ttk.Combobox(window, textvariable=product_var, state="readonly")
    product_dropdown['values'] = get_all_products()
    product_dropdown.pack()

    # Quantity + Price
    tk.Label(window, text="Quantity").pack()
    quantity_entry = tk.Entry(window)
    quantity_entry.pack()

    tk.Label(window, text="Price per Item").pack()
    price_var = tk.StringVar()
    price_entry = tk.Entry(window, textvariable=price_var)
    price_entry.pack()

    def on_product_select(event):
        selected_product = product_var.get()
        price = get_product_price(selected_product)
        price_var.set(str(price))

    product_dropdown.bind("<<ComboboxSelected>>", on_product_select)

    def add_to_cart():
        name = product_var.get()
        if not name:
            messagebox.showerror("Error", "Please select a product")
            return
        try:
            qty = int(quantity_entry.get())
            price = float(price_entry.get())
        except:
            messagebox.showerror("Error", "Enter valid quantity and price")
            return

        cart_items.append((name, qty, qty * price))
        messagebox.showinfo("Added", f"{name} added to cart!")

    def generate_bill():
        if not cart_items:
            messagebox.showerror("Error", "Cart is empty!")
            return

        name = customer_name_entry.get()
        phone = customer_phone_entry.get()
        email = customer_email_entry.get()

        if not name or not phone or not email:
            messagebox.showwarning("Missing Info", "Please fill all customer details.")
            return

        total = sum(item[2] for item in cart_items)

        bill_id = f"BILL{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        generate_bill_pdf(name, phone, email, cart_items, total)

        for item in cart_items:
            update_inventory(item[0], item[1])
        save_to_sales(bill_id, name, cart_items, timestamp)

        messagebox.showinfo("Success", "Bill generated and inventory updated!")

    tk.Button(window, text="Add to Cart", command=add_to_cart).pack(pady=10)
    tk.Button(window, text="Generate Bill", command=generate_bill, bg="green", fg="white").pack(pady=20)
