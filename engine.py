import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum, ARRAY
from uuid import uuid4
import urllib.parse

Base = declarative_base()


class BaseModel:
    def to_dict(self):
        """Returns a dictinary containing all key/values of __dict__"""
        obj_dict = {}
        for key, value in self.__dict__.items():
            obj_dict[key] = value
        return obj_dict
    
    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.id}) {self.__dict__}>"
class Customer(Base, BaseModel):
    __tablename__ = 'customers'
    customer_id = Column(String(40), nullable=False, unique=True, primary_key=True)
    customer_name = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)


class Rider(Base, BaseModel):
    __tablename__ = 'riders'
    rider_id = Column(String(40), nullable=False, primary_key=True)
    rider_name = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False, unique=True)
    number_plate = Column(String(9), nullable=False, unique=False)
    email = Column(String(100), nullable=False, unique=True)
    available = Column(Enum('available', 'on-delivery', 'unavailable'), default='available')


class Product(Base, BaseModel):
    __tablename__ = 'products'
    product_id = Column(Integer, nullable=False, primary_key=True)
    product_name = Column(String(50), nullable=False, unique=True)
    category_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)


class Order(Base, BaseModel):
    __tablename__ = 'orders'
    order_id = Column(String(36), nullable=False, primary_key=True)
    order_items = Column(ARRAY(String(50)), nullable=False)
    customer_id = Column(String(40), nullable=False)
    location = Column(String(50), nullable=False)
    number_of_items = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    total_amount = Column(Integer, nullable=False)


class ProductCategory(Base, BaseModel):
    __tablename__ = 'products_category'
    category_id = Column(Integer, nullable=False, primary_key=True)
    category_name =  Column(String(50), nullable=False)

class Suppliers(Base, BaseModel):
    __tablename__ = 'suppliers'
    supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String(50), nullable=False, unique=True)
    location = Column(String(50), nullable=False)
    products = Column(String(50), nullable=False)


pwd = '!@mElv!s@19'
pwd = urllib.parse.quote(pwd, safe='')
engine = create_engine(f'mysql+mysqldb://root:{pwd}@localhost:3306/wishop')
Base.metadata.create_all(engine)