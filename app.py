from flask import Flask, render_template, request, send_file
import pdf_generator
from database import get_all_products
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    products = get_all_products()
    product_price_map = dict(products)  # {'Milk': 45.0, 'Rice': 60.0, ...}

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        items = []
        for i in range(1, 6):
            pname = request.form.get(f'product{i}')
            qty = request.form.get(f'qty{i}')
            price = request.form.get(f'price{i}')
            if pname and qty and price:
                try:
                    items.append((pname, int(qty), float(price)))
                except:
                    pass

        total = sum(q * p for _, q, p in items)
        filepath = pdf_generator.generate_bill_pdf(name, phone, email, items, total)

        # ✅ Fix MIME type error by giving download_name
        return send_file(filepath, as_attachment=True, download_name=os.path.basename(filepath))

    return render_template('billing.html', products=products, product_prices=product_price_map)

if __name__ == '__main__':
    app.run(debug=True)
