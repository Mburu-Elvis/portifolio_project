from flask import Flask, request, render_template, make_response, jsonify, redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from engine import Base, Customer, Rider, Product, Order, OrderItems, ProductCategory, Delivery
from uuid import uuid4
from datetime import datetime
import urllib


app = Flask(__name__)
pwd = ''
pwd = urllib.parse.quote(pwd)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://root:{pwd}@localhost:3306/wishop'
db = SQLAlchemy(app)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['customer_name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            password = request.form['password']
        except KeyError:
            return render_template('signup.html', error="Please fill in all required fields")
        customer_id = 'cm-' + str(uuid4())
        try:
            new_customer = Customer(
                customer_id=customer_id,
                customer_name=username,
                phone_number=phone_number,
                email=email,
                password=password
            )
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            return render_template('signup.html', error=f"Error: {str(e)}")
    return render_template('signup.html', error=None)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
        except KeyError:
            return render_template('login.html', error="Please fill the required inputs.")
        try:
            customer = db.one_or_404(db.select(Customer).filter_by(email=email))
        except Exception as e:
            return render_template('login.html', error=e)
        if customer.password == password:
            return render_template('dashboard.html')
        return render_template('login.html', error="Incorrect password")
    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/food')
def food():
    print('endpoint queried')
    return render_template('food.html')

@app.route('/customers/password/reset')
def reset_password():
    pass

@app.route('/api/v1.0/customers')
def get_customers():
    '''returns a list of all the customers in the db'''
    with db.session.begin():
        customers = db.session.execute(db.select(Customer).order_by(Customer.customer_name)).scalars()
    if customers:
        customer_list = [customer.to_dict() for customer in customers]
        return jsonify({'customers': customer_list})
    return jsonify({"customers": []})

@app.route('/api/v1.0/customers/<string:customer_id>')
def get_customer(customer_id):
    try:
        customer = db.one_or_404(db.select(Customer).filter_by(customer_id=customer_id))
        return jsonify({'customer': customer.to_dict()})
    except Exception as e:
        return jsonify({"message": "customer doesn't exist"})

@app.route('/api/v1.0/products')
def get_products():
    '''Returns a list of all the products that can be ordered'''
    with db.session.begin():
        products = db.session.execute(db.select(Product).order_by(Product.product_id)).scalars()
    try:
        product_list = [product.to_dict() for product in products]
        return jsonify({'products': product_list})
    except Exception as e:
        return jsonify({"products": []})

@app.route('/api/v1.0/products/<int:product_id>')
def get_product(product_id):
    '''Returns a product of id "id"'''
    try:
        product = db.session.execute(db.select(Product).filter_by(product_id=product_id)).scalar_one()
        return jsonify({'product': product.to_dict()})
    except Exception as e:
            return jsonify({"message": "product not found"})
    
@app.route('/api/v1.0/products/<string:category>')
def get_products_by_category(category):
    '''Returns a list of products belonging to a specific category'''
    try:
        category_id = db.one_or_404(db.select(ProductCategory.category_id).filter_by(category_name=category))
        print(category_id)
        products = db.session.execute(db.select(Product).filter_by(category_id=category_id)).scalars()
        product_list = [product.to_dict() for product in products]
        return jsonify({'products': product_list})
    except Exception as e:
        return jsonify({"message": "category doesn't exist"})

@app.route('/ap1/v1.0/make_order', methods=["POST"])
def make_order():
    data = request.json
    order_id = str(uuid4())
    customer_id = data['customer_id']
    location = data['location']
    total_amount = data['total_amount']
    order_items = data['order_items']
    try:
        new_order = Order(
            order_id = order_id,
            customer_id = customer_id,
            location = location,
            order_date = datetime.now(),
            total_amount = total_amount,
            order_status = 'received'
            )
        db.session.add(new_order)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)})
    for key, value in order_items.items():
        item_id = str(uuid4())
        try:
            new_item = OrderItems(
                order_item_id = item_id,
                order_id = order_id,
                product_id = int(key),
                quantity = value['quantity'],
                price_per_unit = db.one_or_404(db.select(Product.price).filter_by(product_id=int(key))),
                sub_total = value['quantity']*db.one_or_404(db.select(Product.price).filter_by(product_id=int(key)))
            )
            product = db.one_or_404(db.select(Product).filter_by(product_id=key))
            product.quantity -= new_item.quantity
            db.session.add(new_item)
        except Exception as e:
            return jsonify({"message": str(e)})
    db.session.commit()
    return jsonify({"message": "order successful"})

@app.route('/api/v1.0/orders')
def get_orders():
    orders = db.session.execute(db.select(Order).order_by(Order.order_date)).scalars()
    order_list = [order.to_dict() for order in orders]
    return jsonify({'orders': order_list})

@app.route('/api/v1.0/orders/<string:order_id>')
def get_order(order_id):
    try:
        order = db.one_or_404(db.select(Order).filter_by(order_id=order_id))
        return jsonify({"order": order.to_dict()})
    except Exception as e:
        return jsonify({'message': 'order doesn\'t exist'})
    
@app.route('/api/v1.0/customers/orders/<string:customer_id>')
def get_customer_orders(customer_id):
    try:
        customer = db.session.execute(db.select(Customer).filter_by(customer_id=customer_id)).scalar_one()
        customer_id = customer.customer_id
    except Exception as e:
        return jsonify({"message": "customer doesn't exist"})
        
    try:
        orders = db.session.execute(db.select(Order).filter_by(customer_id=customer_id)).scalars()
        order_list = [order.to_dict() for order in orders]
        if order_list == []:
            return jsonify({"message": "customer hasn't made an order yet"})
        return jsonify({"orders": order_list})
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/api/v1.0/riders")
def get_riders():
    with db.session.begin():
        riders = db.session.execute(db.select(Rider).order_by(Rider.rider_name)).scalars()
    rider_list = [rider.to_dict() for rider in riders]
    return jsonify({'riders': rider_list})


@app.route('/api/v1.0/riders/available')
def get_available_riders():
    try:
        riders = db.session.execute(db.select(Rider).filter_by(available='available')).scalars()
        riders_list = [rider.to_dict() for rider in riders]
        if riders_list == []:
            return jsonify({'message': "no rider is currently available"})
        return jsonify({'riders': riders_list})
    except Exception as e:
        return jsonify({"message": str(e)})