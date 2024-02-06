from flask import Flask, request, render_template, make_response, jsonify, redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from engine import Base, Customer, Rider, Product, Order, engine
from uuid import uuid4
import urllib


pwd = urllib.parse.quote(pwd)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://root:{pwd}@localhost:3306/wishop'
db = SQLAlchemy(app)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['customer_name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            password = request.form['password']
        except KeyError:
            return render_template('signup.html', error="Please fill in all required fields")
        
        id = 'cm-' + str(uuid4())
        try:
            new_customer = Customer(
                customer_id = id,
                customer_name=username,
                phone_number = phone_number,
                email = email,
                password = password
            )
            db.session.add(new_customer)
            db.session.commit()
            return render_template('dashboard.html')
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
            return render_template('login.html', error="Incorrect email")
        if customer.password == password:
            return render_template('dashboard.html')
        return render_template('login.html', error="Incorrect password")
    return render_template('login.html', error=None)

@app.route('/food')
def food():
    print('endpoint queried')
    return render_template('food.html')

@app.route('/customers/password/reset')

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
        with db.session.begin():
            product = db.session.execute(db.select(Product).filter_by(product_id=product_id)).scalar_one()
        return jsonify({'product': product.to_dict()})
    except Exception as e:
            return jsonify({"message": "product not found"})
    
@app.route('/api/v1.0/products/<string:category>')
def get_products_by_category(category):
    '''Returns a list of products belonging to a specific category'''
    try:
        with db.session.begin():
            products = db.session.execute(db.select(Product).filter_by(category=category)).scalars()
            product_list = [product.to_dict() for product in products]
        return jsonify({'products': product_list})
    except Exception as e:
        return jsonify({"message": "category doesn't exist"})

@app.route('/api/v1.0/customers')
def get_customers():
    '''returns a list of all the customers in the db'''
    with db.session.begin():
        customers = db.session.execute(db.select(Customer).order_by(Customer.customer_name)).scalars()
    if customer_list:
        customer_list = [customer.to_dict() for customer in customers]
        return jsonify({'customers': customer_list})
    return jsonify({"customers": []})

@app.route('/api/v1.0/customers/<string:email>')
def get_customer(email):
    try:
        with db.session.begin():
            customer = db.session.execute(db.select(Customer).filter_by(email=email)).scalar_one()
        return jsonify({'customer': customer.to_dict()})
    except Exception as e:
        return jsonify({"message": "customer doesn't exist"})

@app.route('/api/v1.0/orders')
def get_orders():
    with db.session.begin():
        orders = db.session.execute(db.select(Order).order_by(Order.date)).scalars()
    order_list = [order.to_dict() for order in orders]
    return jsonify({'orders': order_list})

@app.route('/api/v1.0/orders/<string:order_id>')
def get_order(order_id):
    try:
        with db.session.begin():
            order = db.session.execute(db.select(Order).filter_by(order_id=order_id)).scalar_one()
        return jsonify({'order': order.to_dict()})
    except Exception as e:
        return jsonify({'message': 'order doesn\'t exist'})
    
@app.route('/api/v1.0/orders/<string:customer_id>')
def get_customer_order(customer_id):
    pass


@app.route("/api/v1.0/riders")
def get_riders():
    with db.session.begin():
        riders = db.session.execute(db.select(Rider).order_by(Rider.rider_name)).scalars()
    rider_list = [rider.to_dict() for rider in riders]
    return jsonify({'riders': rider_list})


@app.route('/api/v1.0/riders/available')
def get_available_rider():
    pass

