from flask import Flask, request, render_template, make_response, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from engine import Base, Customer, Rider, Product, Order, engine
from uuid import uuid4
import urllib


app = Flask(__name__)
pwd = ''
pwd = urllib.parse.quote(pwd)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://root:{pwd}@localhost:3306/wishop'
db = SQLAlchemy(app)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    username = request.form['customer_name']
    email = request.form['email']
    phone_number = request.form['phone']
    id = 'cm-' + str(uuid4())
    pwd = '!@mElv!s@19'
    
    pwd = parse.quote(pwd, safe='')
    engine = create_engine(f'mysql+mysqldb://root:{pwd}@localhost:3306/wishop')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    customer = Customer(customer_id=id, customer_name=username, phone_number=phone_number, email=email)
    session.add(customer)
    session.commit()
    session.close()
    return render_template('login.html')