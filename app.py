import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from database.db_connect import get_connection
from dashboard.dashboard import get_dashboard_stats
from werkzeug.utils import secure_filename
from flask import request 

app = Flask(__name__)
app.secret_key = "f7a8d3e2c1b4f9a0d6e7c3b8a1f2e9d5"

BASE_IMAGE_UPLOAD_FOLDER = 'static/images/products'

CATEGORY_FOLDERS = {
    "Electronics Gadgets": "electronics-gadgets",
    "Mobile Phones": "mobile-phones",
    "Computers & Laptops": "computers-laptops",
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
        {"name": "Computers & Laptops", "folder": "computers-laptops"},
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
        "Computers & Laptops": "products_computers_laptops",
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


@app.route('/user/profile')
def user_profile():
    return render_template('user/profile.html')

@app.route('/products')
def products_list():
    return render_template('products/list.html')

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    conn = get_connection()             # ডাটাবেস কানেকশন নাও
    cursor = conn.cursor(dictionary=True)  # কার্সর তৈরি করো

    cursor.execute("SELECT * FROM imported_products WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()

    if not product:
        return "Product not found", 404
    return render_template("product_detail.html", product=product)


# Computer and Laptop Products (আগেই ছিল)
@app.route('/products/computers-laptops')
def products_computers_laptops():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    offset = (page - 1) * per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM imported_products WHERE category = %s", ("Computers & Laptops",))
    total_products = cursor.fetchone()['total']
    cursor.execute("""
        SELECT * FROM imported_products 
        WHERE category = %s 
        ORDER BY created_at DESC 
        LIMIT %s OFFSET %s
    """, ("Computers & Laptops", per_page, offset))
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




@app.route('/orders')
def orders_list():
    return render_template('orders/order_list.html')

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/api/dashboard_stats')
def dashboard_stats_api():
    stats = get_dashboard_stats()
    return jsonify(stats)

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

if __name__ == '__main__':
    app.run(debug=True)
