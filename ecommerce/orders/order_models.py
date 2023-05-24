from datetime import datetime

from sqlalchemy import Integer, Column, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from ecommerce.user.user_models import User
from ecommerce.products.product_models import Product

from ecommerce.db import Base


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, default=datetime.now)
    order_amount = Column(Float, default=0.0)
    order_status = Column(String(50), default='PROCESSING')
    shipping_address = Column(Text)
    customer_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    order_details = relationship('OrderDetails', back_populates='order')
    user_info = relationship('User', back_populates='order')


class OrderDetails(Base):
    __tablename__ = 'order_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey(Order.id, ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey(Product.id, ondelete='CASCADE'))
    order = relationship('Order', back_populates='order_details')
    product_order_details = relationship('Product', back_populates='order_details')
    quantity = Column(Integer, default=1)
    created = Column(DateTime, default=datetime.now)