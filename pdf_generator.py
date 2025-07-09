from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.image("static/logo.png", 10, 8, 20)  # ✅ Adjusted to use static/logo.png
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Grocery Store Billing", ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, "Thank you for shopping with us ", ln=True, align="C")
        self.ln(10)

def generate_bill_pdf(name, phone, email, items, total):
    bill_id = "BILL" + datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"Invoice_{bill_id}.pdf"
    os.makedirs("invoices", exist_ok=True)

    subtotal = sum(i[2] for i in items)
    tax = round(subtotal * 0.05, 2)
    grand_total = round(subtotal + tax, 2)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, "SMART GROCERY STORE", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Python Billing System", ln=True, align='C')

    pdf.set_draw_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Bill No       : {bill_id}", ln=True)
    pdf.cell(0, 8, f"Date & Time   : {now}", ln=True)
    pdf.cell(0, 8, f"Customer Name : {name}", ln=True)
    pdf.cell(0, 8, f"Phone Number  : {phone}", ln=True)
    pdf.cell(0, 8, f"Email ID      : {email}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(60, 10, "Product", 1, 0, 'C', fill=True)
    pdf.cell(40, 10, "Quantity", 1, 0, 'C', fill=True)
    pdf.cell(50, 10, "Price", 1, 1, 'C', fill=True)

    pdf.set_font("Arial", '', 11)
    for item in items:
        name_, qty, price = item
        pdf.cell(60, 10, name_, 1)
        pdf.cell(40, 10, str(qty), 1, 0, 'C')
        pdf.cell(50, 10, f"Rs. {price}", 1, 1, 'C')

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(150, 10, "Subtotal", 1)
    pdf.cell(40, 10, f"Rs. {subtotal}", 1, 1, 'C')

    pdf.cell(150, 10, "GST (5%)", 1)
    pdf.cell(40, 10, f"Rs. {tax}", 1, 1, 'C')

    pdf.cell(150, 10, "Total Amount", 1)
    pdf.cell(40, 10, f"Rs. {grand_total}", 1, 1, 'C')

    pdf.ln(10)
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 10, "Thank you for shopping with us!", ln=True, align='C')
    pdf.cell(0, 10, "Visit Again - Smart Grocery Store", ln=True, align='C')

    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 10, "Powered by Python | Developed by Hrushi", ln=True, align='C')

    output_path = os.path.join("invoices", file_name)
    pdf.output(output_path)

    return output_path  # ✅ VERY IMPORTANT for Flask to download
