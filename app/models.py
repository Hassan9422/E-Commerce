# in this file we are gonna store our postgres tables as python classes:
from sqlalchemy import Column, Integer, String, text, TIMESTAMP, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, column_property

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(Integer, unique=True, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    original_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    new_price = column_property((1-discount)*original_price)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    product_owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship('User')
