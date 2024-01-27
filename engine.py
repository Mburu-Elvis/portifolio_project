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

class Rider(Base):
    __tablename__ = 'riders'
    rider_id = Column(String(40), nullable=False, primary_key=True)
    rider_name = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False, unique=True)
    number_plate = Column(String(9), nullable=False, unique=False)
    email = Column(String(100), nullable=False, unique=True)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, nullable=False, primary_key=True)
    product_name = Column(String(50), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(String(36), nullable=False, primary_key=True)
    # customer_id = Column(String(40), ForeignKey=('customers.customer_id'), nullable=False)
    number_of_items = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    total_amount = Column(Integer, nullable=False)

pwd = '!@mElv!s@19'
pwd = urllib.parse.quote(pwd, safe='')
engine = create_engine(f'mysql+mysqldb://root:{pwd}@localhost:3306/wishop')
Base.metadata.create_all(engine)