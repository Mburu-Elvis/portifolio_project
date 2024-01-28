import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from uuid import uuid4
import urllib.parse

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(String(40), nullable=False, unique=True, primary_key=True)
    customer_name = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    
    def to_dict(self):
        return {
            'customer_name': self.customer_name,
            'phone_number': self.customer_name,
            'email': self.email,
            'password': self.password
        }

class Rider(Base):
    __tablename__ = 'riders'
    rider_id = Column(String(40), nullable=False, primary_key=True)
    rider_name = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False, unique=True)
    number_plate = Column(String(9), nullable=False, unique=False)
    email = Column(String(100), nullable=False, unique=True)
    
    def to_dict(self):
        return {
            'rider_name': self.rider_name,
            'phone_number': self.phone_number,
            'number_plate': self.number_plate,
            'email': self.email
        }

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, nullable=False, primary_key=True)
    product_name = Column(String(50), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'price': self.price,
            'quantity': self.quantity
        }

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(String(36), nullable=False, primary_key=True)
    # customer_id = Column(String(40), ForeignKey=('customers.customer_id'), nullable=False)
    number_of_items = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    total_amount = Column(Integer, nullable=False)
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'number_of_items': self.number_of_items,
            'date': self.date,
            'total_amount': self.total_amount
        }

pwd = '!@mElv!s@19'
pwd = urllib.parse.quote(pwd, safe='')
engine = create_engine(f'mysql+mysqldb://root:{pwd}@localhost:3306/wishop')
Base.metadata.create_all(engine)