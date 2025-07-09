# grocery_billing_system
A full grocery store billing system with Python, SQLite, Flask, PDF, and Dashboard.

🛒 Grocery Store Billing & Inventory System
A full-featured desktop + web-based billing system for managing a grocery store, built using Python, SQLite, Flask, FPDF, and Matplotlib.
This project supports real-time billing, inventory tracking, PDF invoice generation, dashboard analytics, and a user-friendly web interface.

Features:
> Admin Panel (Add / Update / Delete products)
> Live Inventory Management (auto-update after billing)
> Customer Billing with Product Dropdowns & Auto Price Fill
> PDF Invoice Generation (with Logo, Store Name, Tax, Total)
> Graphical Dashboard (Low Stock & Top Selling Products)
> Web Interface using Flask + HTML/CSS
> Clean Light UI (with optional Dark Mode)
> Role-based Login System (optional)
> CSV Report Export, Print Support

Tech Stack:
Frontend : Tkinter, HTML, CSS
Backend	: Python, Flask
Database :	SQLite
PDF Gen :	FPDF (for invoice generation)
Graphs :	Matplotlib
IDE	: VS Code

📂 Folder Structure:
📁 grocery_billing_system/
├── main.py
├── admin.py
├── billing.py
├── dashboard.py
├── reports.py
├── database.py
├── pdf_generator.py
├── login.py (optional)
├── templates/
│   ├── base.html
│   ├── billing.html
│   ├── dashboard.html
│   └── ...
├── static/
│   ├── style.css
│   └── logo.png
├── invoices/
│   └── PDF bills
├── screenshots/
│   └── billing_ui.png, invoice_pdf.png, dashboard.png
├── README.md


Sample Invoice (PDF): 

SMART GROCERY STORE
Invoice ID: BILL202507091805
Customer: Hrushi
Phone: 9876543210

Product        Qty     Price
----------     ---     ------
Rice           2       ₹80
Sugar          1       ₹40

GST (5%)       ₹6
TOTAL          ₹126

Thank you for shopping 
Visit Again!
Dashboard Preview
Low Stock Alert: Shows products with quantity < 5
Top Sellers: Graphical view of most sold items

💡 How to Run
> Desktop (Tkinter GUI):
python main.py
> Web Version (Flask UI):
python app.py
> Then open browser:
http://127.0.0.1:5000/


To-Do / Future Enhancements:
> Role-based login system (Admin vs Cashier)
> Barcode scanner support
> Product thumbnails
> Monthly sales reports
> Cloud deployment (Render/Vercel)


Developed By : Sai Hrushita Kolachina
NIT Raipur | ECE
Passionate about Python, AI, and Automation
saihrushita2508@gmail.com
