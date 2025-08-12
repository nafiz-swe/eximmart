import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from database.db_connect import get_connection
from dashboard.dashboard import get_dashboard_stats
from werkzeug.utils import secure_filename
from flask import request 
from flask import session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "f7a8d3e2c1b4f9a0d6e7c3b8a1f2e9d5"

BASE_IMAGE_UPLOAD_FOLDER = 'static/images/products'

CATEGORY_FOLDERS = {
    "Electronics Gadgets": "electronics-gadgets",
    "Mobile Phones": "mobile-phones",
    "Computer & Laptop": "computers-laptops",
    "Toys & Kids": "toys-kids",
    "Fashion & Wear": "fashion-wear",
    "Beauty & Cosmetics": "beauty-cosmetics",
    "Home Decor": "home-decor",
    "Plastics & Homeware": "plastics-homeware",
    "Kitchen Appliances": "kitchen-appliances",
    "Lighting": "lighting",
    "Vehicle Accessories": "vehicle-accessories",
    "Fitness & Sports": "fitness-sports",
    "Health & Care": "health-care",
    "Office & School": "office-school",
    "Farming Tools": "farming-tools"
}

# Create folders if not exist (optional)
for folder in CATEGORY_FOLDERS.values():
    os.makedirs(os.path.join(BASE_IMAGE_UPLOAD_FOLDER, folder), exist_ok=True)




@app.route('/')
def dashboard_page():
    categories = [
        {"name": "Electronics Gadgets", "folder": "electronics-gadgets"},
        {"name": "Mobile Phones", "folder": "mobile-phones"},
        {"name": "Computer & Laptop", "folder": "computers-laptops"},
        {"name": "Toys & Kids", "folder": "toys-kids"},
        {"name": "Fashion & Wear", "folder": "fashion-wear"},
        {"name": "Beauty & Cosmetics", "folder": "beauty-cosmetics"},
        {"name": "Home Decor", "folder": "home-decor"},
        {"name": "Plastics & Homeware", "folder": "plastics-homeware"},
        {"name": "Kitchen Appliances", "folder": "kitchen-appliances"},
        {"name": "Lighting", "folder": "lighting"},
        {"name": "Vehicle Accessories", "folder": "vehicle-accessories"},
        {"name": "Fitness & Sports", "folder": "fitness-sports"},
        {"name": "Health & Care", "folder": "health-care"},
        {"name": "Office & School", "folder": "office-school"},
        {"name": "Farming Tools", "folder": "farming-tools"},
    ]

    CATEGORY_ROUTE_NAMES = {
        "Electronics Gadgets": "products_gadgets",
        "Mobile Phones": "products_mobile_phones",
        "Computer & Laptop": "products_computers_laptops",
        "Toys & Kids": "products_toys_kids",
        "Fashion & Wear": "products_fashion_wear",
        "Beauty & Cosmetics": "products_beauty_cosmetics",
        "Home Decor": "products_home_decor",
        "Plastics & Homeware": "products_plastics_homeware",
        "Kitchen Appliances": "products_kitchen_appliances",
        "Lighting": "products_lighting",
        "Vehicle Accessories": "products_vehicle_accessories",
        "Fitness & Sports": "products_fitness_sports",
        "Health & Care": "products_health_care",
        "Office & School": "products_office_school",
        "Farming Tools": "products_farming_tools"
    }

    page = request.args.get('page', 1, type=int)
    per_page = 24
    offset = (page - 1) * per_page

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM imported_products")
    total_products = cursor.fetchone()['total']

    cursor.execute("""
        SELECT * FROM imported_products 
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    total_pages = (total_products + per_page - 1) // per_page

    return render_template('index.html', categories=categories, products=products, route_names=CATEGORY_ROUTE_NAMES,
                           page=page, total_pages=total_pages)



# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login first!")
        return redirect(url_for('login_page'))

    quantity = request.form.get('quantity', 1)
    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except:
        quantity = 1

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get product info
    cursor.execute("SELECT * FROM imported_products WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        cursor.close()
        conn.close()
        flash("Product not found!")
        return redirect(url_for('dashboard_page'))

    # ✅ Stock check
    if quantity > product['stock']:
        flash(f"Only {product['stock']} items available in stock.")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard_page'))

    product_name = product['product_name']
    unit_price = float(product['price'])

    cursor.execute("SELECT users_mobile FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    users_mobile = user['users_mobile'] if user else ""

    cursor.execute("""
        SELECT cart_id, quantity FROM cart
        WHERE users_id = %s AND product_id = %s
    """, (user_id, product_id))
    existing = cursor.fetchone()

    if existing:
        new_quantity = existing['quantity'] + quantity

        # ✅ Stock check for updated quantity
        if new_quantity > product['stock']:
            flash(f"Cannot add more than {product['stock']} items to cart.")
            cursor.close()
            conn.close()
            return redirect(url_for('cart_page'))

        new_total = unit_price * new_quantity
        cursor.execute("""
            UPDATE cart SET quantity = %s, total_price = %s, added_at = NOW()
            WHERE cart_id = %s
        """, (new_quantity, new_total, existing['cart_id']))
    else:
        total_price = unit_price * quantity
        cursor.execute("""
            INSERT INTO cart
            (users_id, users_mobile, product_id, product_name, unit_price, quantity, total_price, added_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """, (user_id, users_mobile, product_id, product_name, unit_price, quantity, total_price))

    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Added {quantity} x {product_name} to your cart.")
    return redirect(url_for('cart_page'))



@app.route('/cart')
def cart_page():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login first!")
        return redirect(url_for('login_page'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cart WHERE users_id = %s", (user_id,))
    cart_items = cursor.fetchall()
    cursor.close()
    conn.close()

    total_price = sum(item['total_price'] for item in cart_items)
    total_quantity = sum(item['quantity'] for item in cart_items)
    total_categories = len(set(item['product_name'] for item in cart_items))

    return render_template(
        'orders/cart.html',
        cart_items=cart_items,
        total_price=total_price,
        total_quantity=total_quantity,
        total_categories=total_categories
    )


@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Login required'}), 401

    cart_id = request.form.get('cart_id')
    quantity = request.form.get('quantity')
    try:
        quantity = int(quantity)
        if quantity < 1:
            return jsonify({'error': 'Quantity must be at least 1'}), 400
    except:
        return jsonify({'error': 'Invalid quantity'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get cart & product info
    cursor.execute("""
        SELECT c.unit_price, c.product_id, p.stock 
        FROM cart c
        JOIN imported_products p ON c.product_id = p.id
        WHERE c.cart_id=%s AND c.users_id=%s
    """, (cart_id, user_id))
    res = cursor.fetchone()
    if not res:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Cart item not found'}), 404

    # ✅ Stock check
    if quantity > res['stock']:
        cursor.close()
        conn.close()
        return jsonify({'error': f"Only {res['stock']} items available in stock."}), 400

    unit_price = res['unit_price']
    total_price = unit_price * quantity

    cursor.execute("""
        UPDATE cart SET quantity=%s, total_price=%s, added_at=NOW()
        WHERE cart_id=%s AND users_id=%s
    """, (quantity, total_price, cart_id, user_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'success': True, 'new_total': f"{total_price:.2f}"})



@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login first!")
        return redirect(url_for('login_page'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE cart_id = %s AND users_id = %s", (cart_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Product removed from cart.")
    return redirect(url_for('cart_page'))


@app.context_processor
def inject_cart_count():
    user_id = session.get('user_id')
    if not user_id:
        return dict(cart_count=0)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT product_id) FROM cart WHERE users_id = %s", (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return dict(cart_count=count)



@app.route('/order', methods=['GET', 'POST'])
def order_page():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login first!")
        return redirect(url_for('login_page'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cart WHERE users_id = %s", (user_id,))
    cart_items = cursor.fetchall()
    cursor.close()
    conn.close()

    if not cart_items:
        flash("Your cart is empty! Please add products before placing an order.")
        return redirect(url_for('cart_page'))

    total_price = sum(item['total_price'] for item in cart_items)
    total_quantity = sum(item['quantity'] for item in cart_items)
    total_categories = len(set(item['product_name'] for item in cart_items))

    if request.method == 'POST':
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        id_proof_type = request.form.get('idProofType')

        if id_proof_type == 'nid':
            id_number = request.form.get('nidNumber')
            id_file_upload = request.files.get('nidFile')
        elif id_proof_type == 'passport':
            id_number = request.form.get('passportNumber')
            id_file_upload = request.files.get('passportFile')
        else:
            id_number = None
            id_file_upload = None

        payment_method = request.form.get('paymentMethod')

        id_file_path = None
        if id_file_upload and allowed_file(id_file_upload.filename):
            filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{id_file_upload.filename}")
            upload_folder = os.path.join(app.root_path, 'static', 'images', 'orders')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            id_file_upload.save(file_path)
            id_file_path = f'images/orders/{filename}'

        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO orders (
                        user_name, user_email, user_mobile, shipping_address,
                        id_proof_type, id_number, id_file_path, payment_method,
                        total_categories, total_quantity, total_price, order_status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    full_name, email, phone, address,
                    id_proof_type, id_number, id_file_path, payment_method,
                    total_categories, total_quantity, total_price, 'pending'  # নতুন কলাম এ 'pending' ডিফল্ট স্ট্যাটাস
                ))
                conn.commit()

                # অর্ডার সফল হলে কার্ট খালি করে দাও
                cursor.execute("DELETE FROM cart WHERE users_id = %s", (user_id,))
                conn.commit()

        except Exception as e:
            flash(f"Error placing order: {e}", "danger")
            return redirect(url_for('order_page'))
        finally:
            conn.close()

        flash("Order placed successfully!", "success")
        return redirect(url_for('dashboard_page'))

    return render_template(
        'orders/order.html',
        cart_items=cart_items,
        total_price=total_price,
        total_quantity=total_quantity,
        total_categories=total_categories
    )




# Computer and Laptop Products (আগেই ছিল)
@app.route('/products/computers-laptops')
def products_computers_laptops():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    offset = (page - 1) * per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Computer & Laptop",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products 
        WHERE category = %s 
        ORDER BY created_at DESC 
        LIMIT %s OFFSET %s
    """, ("Computer & Laptop", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products + per_page - 1) // per_page
    return render_template('products/computers-laptops.html', 
                           products=products, page=page, total_pages=total_pages)


# Mobile Phones
@app.route('/products/mobile-phones')
def products_mobile_phones():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    offset = (page -1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Mobile Phones",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Mobile Phones", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products + per_page -1)//per_page
    return render_template('products/mobile-phones.html', products=products, page=page, total_pages=total_pages)


# Gadgets
@app.route('/products/gadgets')
def products_gadgets():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    offset = (page -1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Electronics Gadgets",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Electronics Gadgets", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products + per_page -1)//per_page
    return render_template('products/gadgets.html', products=products, page=page, total_pages=total_pages)


# Plastics & Homeware
@app.route('/products/plastics-homeware')
def products_plastics_homeware():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Plastics & Homeware",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Plastics & Homeware", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/plastics-homeware.html', products=products, page=page, total_pages=total_pages)


# Toys & Kids
@app.route('/products/toys-kids')
def products_toys_kids():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Toys & Kids",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Toys & Kids", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/toys-kids.html', products=products, page=page, total_pages=total_pages)


# Home Decor
@app.route('/products/home-decor')
def products_home_decor():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Home Decor",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Home Decor", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/home-decor.html', products=products, page=page, total_pages=total_pages)


# Lighting
@app.route('/products/lighting')
def products_lighting():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Lighting",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Lighting", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/lighting.html', products=products, page=page, total_pages=total_pages)


# Farming Tools
@app.route('/products/farming-tools')
def products_farming_tools():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Farming Tools",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Farming Tools", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/farming-tools.html', products=products, page=page, total_pages=total_pages)


# Kitchen Appliances
@app.route('/products/kitchen-appliances')
def products_kitchen_appliances():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Kitchen Appliances",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Kitchen Appliances", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/kitchen-appliances.html', products=products, page=page, total_pages=total_pages)


# Fitness & Sports
@app.route('/products/fitness-sports')
def products_fitness_sports():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Fitness & Sports",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Fitness & Sports", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/fitness-sports.html', products=products, page=page, total_pages=total_pages)


# Health & Care
@app.route('/products/health-care')
def products_health_care():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Health & Care",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Health & Care", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/health-care.html', products=products, page=page, total_pages=total_pages)


# Office & School
@app.route('/products/office-school')
def products_office_school():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Office & School",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Office & School", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/office-school.html', products=products, page=page, total_pages=total_pages)


# Vehicle Accessories
@app.route('/products/vehicle-accessories')
def products_vehicle_accessories():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Vehicle Accessories",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Vehicle Accessories", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/vehicle-accessories.html', products=products, page=page, total_pages=total_pages)


# Fashion & Wear
@app.route('/products/fashion-wear')
def products_fashion_wear():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Fashion & Wear",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Fashion & Wear", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/fashion-wear.html', products=products, page=page, total_pages=total_pages)


# Beauty & Cosmetics
@app.route('/products/beauty-cosmetics')
def products_beauty_cosmetics():
    page = request.args.get('page',1,type=int)
    per_page = 24
    offset = (page-1)*per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Beauty & Cosmetics",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products
        WHERE category = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, ("Beauty & Cosmetics", per_page, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total_products+per_page-1)//per_page
    return render_template('products/beauty-cosmetics.html', products=products, page=page, total_pages=total_pages)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms_and_conditions')
def terms_and_conditions():
    return render_template('terms_and_conditions.html')




@app.route('/user/account')
def user_account():
    if 'user_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ইউজারের পুরো তথ্য নিয়ে আসা
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    # অর্ডার নিয়ে আসা, order_status স্ট্রিং হিসেবে আসবে
    cursor.execute("""
        SELECT * FROM orders WHERE user_email = %s ORDER BY order_date DESC
        """, (user['users_email'],))
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('user/account.html',
                           user_name=user['users_name'],
                           user_email=user['users_email'],
                           user_mobile=user['users_mobile'],
                           user_profession=user['users_profession'],
                           user_created=user['users_create_account'].strftime('%Y-%m-%d'),
                           orders=orders)




@app.route('/login', methods=['GET', 'POST'])
def login():
    # যদি ইউজার already logged in থাকে
    if 'user_id' in session:
        return redirect(url_for('user_account'))

    if request.method == 'POST':
        login_input = request.form.get('login_input', '').strip()
        password = request.form.get('password', '').strip()

        if not login_input or not password:
            flash("Both email/phone and password are required.", "error")
            return redirect(url_for('login'))

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if '@' in login_input:
            cursor.execute("SELECT * FROM users WHERE users_email = %s", (login_input,))
            user_type = "email"
        else:
            cursor.execute("SELECT * FROM users WHERE users_mobile = %s", (login_input,))
            user_type = "phone"

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            flash(f"No user found with this {user_type}.", "error")
            return redirect(url_for('login'))

        if not check_password_hash(user['users_password'], password):
            flash("Incorrect password.", "error")
            return redirect(url_for('login'))

        # সেশন-এ সব তথ্য রাখলাম
        session['user_id'] = user['id']
        session['user_name'] = user['users_name']
        session['user_email'] = user['users_email']
        session['user_mobile'] = user['users_mobile']
        session['user_profession'] = user['users_profession']
        # টাইমস্ট্যাম্প কে স্ট্রিং এ রূপান্তর
        session['user_created'] = user['users_create_account'].strftime('%Y-%m-%d %H:%M:%S')

        flash("Logged in successfully!", "success")
        return redirect(url_for('user_account'))

    return render_template('user/login.html')




@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))




@app.route('/register', methods=['GET', 'POST'])
def register():
    # যদি ইউজার already logged in থাকে
    if 'user_id' in session:
        return redirect(url_for('user_account'))

    if request.method == 'POST':
        users_name = request.form.get('users_name').strip()
        users_email = request.form.get('users_email').strip()
        users_mobile = request.form.get('users_mobile').strip()
        users_profession = request.form.get('users_profession').strip()
        users_password = request.form.get('users_password')
        confirm_password = request.form.get('confirm_password')

        if users_password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))

        import re
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$')
        if not regex.match(users_password):
            flash("Password must be at least 6 characters and include uppercase, lowercase, number, and special character.", "error")
            return redirect(url_for('register'))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE users_email = %s OR users_mobile = %s", (users_email, users_mobile))
        existing = cursor.fetchone()
        if existing:
            flash("User with this email or mobile number already exists.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('register'))

        # Hash the password before storing
        hashed_password = generate_password_hash(users_password)

        insert_sql = """
            INSERT INTO users (users_name, users_email, users_mobile, users_profession, users_password) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (users_name, users_email, users_mobile, users_profession, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Registration successful! You can now login.", "success")
        return redirect(url_for('login'))

    return render_template('user/register.html')



@app.route('/api/dashboard_stats')
def dashboard_stats_api():
    stats = get_dashboard_stats()
    return jsonify(stats)



@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM imported_products WHERE id = %s"
    cursor.execute(sql, (product_id,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()

    if not product:
        flash("Product not found.", "error")
        return redirect(url_for('dashboard_page'))  # অথবা তোমার হোম পেজ

    return render_template('product_detail.html', product=product)


@app.route('/products/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        category = request.form.get('category')
        if category not in CATEGORY_FOLDERS:
            flash("Invalid category selected.", "error")
            return redirect(request.url)

        product_name = request.form.get('product_name')
        brand_name = request.form.get('brand_name')
        product_color = request.form.get('product_color')
        description = request.form.get('description')
        price = request.form.get('price')
        stored_in = request.form.get('stored_in')
        stock = request.form.get('stock') or 0
        sold = request.form.get('sold') or 0
        factory_shop_address = request.form.get('factory_shop_address')
        contact_number = request.form.get('contact_number')
        product_owner_name = request.form.get('product_owner_name')

        image1 = request.files.get('product_image1')
        if not image1 or image1.filename == '':
            flash("Product Image 1 is required!", "error")
            return redirect(request.url)

        category_folder = CATEGORY_FOLDERS[category]
        save_folder = os.path.join(BASE_IMAGE_UPLOAD_FOLDER, category_folder)

        # Save required image1
        image1_filename = secure_filename(image1.filename)
        image1_path = os.path.join(save_folder, image1_filename)
        image1.save(image1_path)

        # Optional images and video
        image2 = request.files.get('product_image2')
        image3 = request.files.get('product_image3')
        video = request.files.get('product_video')

        image2_filename = None
        image3_filename = None
        video_filename = None

        if image2 and image2.filename != '':
            image2_filename = secure_filename(image2.filename)
            image2_path = os.path.join(save_folder, image2_filename)
            image2.save(image2_path)

        if image3 and image3.filename != '':
            image3_filename = secure_filename(image3.filename)
            image3_path = os.path.join(save_folder, image3_filename)
            image3.save(image3_path)

        if video and video.filename != '':
            video_filename = secure_filename(video.filename)
            video_path = os.path.join(save_folder, video_filename)
            video.save(video_path)

        image1_db_path = f'images/products/{category_folder}/{image1_filename}'
        image2_db_path = f'images/products/{category_folder}/{image2_filename}' if image2_filename else None
        image3_db_path = f'images/products/{category_folder}/{image3_filename}' if image3_filename else None
        video_db_path = f'images/products/{category_folder}/{video_filename}' if video_filename else None

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO imported_products 
        (category, product_name, brand_name, product_color, description, price, stored_in, stock, sold, factory_shop_address, contact_number, product_owner_name, 
        product_image1, product_image2, product_image3, product_video, import_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())
        """
        values = (
            category, product_name, brand_name, product_color, description, price, stored_in, stock, sold,
            factory_shop_address, contact_number, product_owner_name,
            image1_db_path, image2_db_path, image3_db_path, video_db_path
        )

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        flash("Product added successfully!", "success")
        return redirect(url_for('add_product'))

    return render_template('products/add_product.html')




@app.route('/search', methods=['GET', 'POST'])
def search_products():
    search_query = request.args.get('q', '').strip()
    image_file = request.files.get('image')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search_query:
        words = search_query.split()

        conditions = []
        params = []
        for word in words:
            condition = """
                (category REGEXP %s OR product_name REGEXP %s OR brand_name REGEXP %s)
            """
            conditions.append(condition)
            regex_pattern = f'[[:<:]]{word}[[:>:]]'
            params.extend([regex_pattern, regex_pattern, regex_pattern])

        where_clause = " OR ".join(conditions)

        sql = f"""
            SELECT *,
                (
                    { " + ".join([f"(category REGEXP %s) + (product_name REGEXP %s) + (brand_name REGEXP %s)" for _ in words]) }
                ) AS match_count
            FROM imported_products
            WHERE {where_clause}
            ORDER BY match_count DESC, product_name ASC
        """

        match_params = []
        for word in words:
            regex_pattern = f'[[:<:]]{word}[[:>:]]'
            match_params.extend([regex_pattern, regex_pattern, regex_pattern])

        cursor.execute(sql, match_params + params)
        products = cursor.fetchall()

    elif image_file:
        # ইমেজ সার্চ logic ekhane thakbe (optional)
        cursor.execute("SELECT * FROM imported_products LIMIT 50")
        products = cursor.fetchall()

    else:
        products = []

    cursor.close()
    conn.close()

    return render_template('products/search.html', products=products, query=search_query)



if __name__ == '__main__':
    app.run(debug=True)
