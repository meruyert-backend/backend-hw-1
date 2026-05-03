from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Float
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Flower(Base):
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id"))
    quantity = Column(Integer, default=1)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id"))