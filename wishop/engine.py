import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship
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
            if not key.startswith('_') and not isinstance(value, sqlalchemy.orm.collections.InstrumentedList):
                obj_dict[key] = value
        return obj_dict
    
    def __repr__(self):
        return f"<[{self.__class__.__name__}] {self.__dict__}>"


class Customer(Base, BaseModel):
    __tablename__ = 'customers'

    customer_id = Column(String(40), nullable=False, unique=True, primary_key=True)
    customer_name = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    orders = relationship("Order", back_populates="customer")


class Order(Base, BaseModel):
    __tablename__ = 'orders'

    order_id = Column(String(36), nullable=False, primary_key=True)
    customer_id = Column(String(40), ForeignKey('customers.customer_id'),nullable=False) 
    location = Column(String(50), nullable=False)
    order_date = Column(DateTime, nullable=False)
    total_amount = Column(Integer, nullable=False)
    order_status = Column(Enum("received", "processed", "on-delivery", "delivered"))

    customer = relationship("Customer", back_populates='orders')
    order_items = relationship("OrderItems", back_populates="order")
    delivery = relationship("Delivery", back_populates="order")


class OrderItems(Base, BaseModel):
    __tablename__ = 'order_items'

    order_item_id = Column(String(36), primary_key=True)
    order_id = Column(String(36), ForeignKey('orders.order_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Integer, nullable=False)
    sub_total = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

class Product(Base, BaseModel):
    __tablename__ = 'products'

    product_id = Column(Integer, nullable=False, primary_key=True)
    product_name = Column(String(50), nullable=False, unique=True)
    description = Column(String(1000), nullable=False)
    category_id = Column(Integer, ForeignKey('products_category'), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    category = relationship("ProductCategory", back_populates="product")
    order_items = relationship("OrderItems", back_populates="product")

class ProductCategory(Base, BaseModel):
    __tablename__ = 'products_category'

    category_id = Column(Integer, nullable=False, primary_key=True)
    category_name =  Column(String(50), nullable=False)

    product = relationship("Product", back_populates="category")

class Rider(Base, BaseModel):
    __tablename__ = 'riders'

    rider_id = Column(String(40), nullable=False, primary_key=True)
    rider_name = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False, unique=True)
    number_plate = Column(String(9), nullable=False, unique=False)
    email = Column(String(100), nullable=False, unique=True)
    available = Column(Enum('available', 'on-delivery', 'unavailable'), default='available')

    delivery = relationship("Delivery", back_populates="rider")


class Delivery(Base, BaseModel):
    __tablename__ = 'delivery'

    delivery_id = Column(String(40), primary_key=True)
    date_time = Column(DateTime, nullable=False)
    order_id = Column(String(40), ForeignKey('orders.order_id'))
    rider_id = Column(String(40), ForeignKey('riders.rider_id'))
    payment_message = Column(String(40), nullable=False, unique=True)

    order = relationship("Order", back_populates="delivery")
    rider = relationship("Rider", back_populates="delivery")


username = ''
pwd = ''
db = ''

engine = create_engine(f'mysql+mysqldb://{username}:{pwd}@localhost:3306/{db}')
Base.metadata.create_all(engine)