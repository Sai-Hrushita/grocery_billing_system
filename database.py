import sqlite3

def create_tables():
    conn = sqlite3.connect("grocery.db")
    cur = conn.cursor()

    # ✅ Products Table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        quantity INTEGER
    )
    ''')

    # ✅ Sales Table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id TEXT,
        customer_name TEXT,
        product_name TEXT,
        quantity INTEGER,
        total_price REAL,
        date TEXT
    )
    ''')

    # ✅ Users Table for Login
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
    )
    ''')

    # ✅ Insert default admin if not exists
    cur.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', 'admin123', 'admin'))

    conn.commit()
    conn.close()
    print("✅ Database and tables created successfully.")

# ✅ Inventory Update Function
def update_inventory(product_name, quantity_sold):
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()

    cursor.execute("SELECT quantity FROM products WHERE name = ?", (product_name,))
    result = cursor.fetchone()

    if result:
        current_qty = result[0]
        new_qty = max(0, current_qty - quantity_sold)
        cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", (new_qty, product_name))

    conn.commit()
    conn.close()

# ✅ Save Sales Record Function
def save_to_sales(bill_id, customer_name, items, date):
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    for item in items:
        product_name, qty, total = item
        cursor.execute("""
            INSERT INTO sales (bill_id, customer_name, product_name, quantity, total_price, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (bill_id, customer_name, product_name, qty, total, date))
    conn.commit()
    conn.close()
    
def get_all_products():
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products")
    data = cursor.fetchall()
    conn.close()
    return data

# Run only once to create tables
if __name__ == "__main__":
    create_tables()
