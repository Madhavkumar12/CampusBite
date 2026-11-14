from .database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
import datetime


class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  role = Column(
      String, nullable=False
  )  # Customer, Restaurant Owner, Delivery Partner


class Restaurant(Base):
  __tablename__ = "restaurants"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  owner_id = Column(Integer, ForeignKey("users.id"))
  menu_items = relationship("MenuItem", back_populates="restaurant")
  orders = relationship("Order", back_populates="restaurant")


class MenuItem(Base):
  __tablename__ = "menu_items"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  is_available = Column(Integer, default=1)
  restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
  restaurant = relationship("Restaurant", back_populates="menu_items")


class Order(Base):
  __tablename__ = "orders"
  id = Column(Integer, primary_key=True, index=True)
  customer_id = Column(Integer, ForeignKey("users.id"))
  restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
  delivery_partner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
  status = Column(
      String, default="PLACED"
  )  # PLACED, ACCEPTED, PREPARING, READY, ASSIGNED, OUT_FOR_DELIVERY, DELIVERED, CANCELLED
  total_price = Column(Float, nullable=False)
  payment_status = Column(String, default="MOCK_PAID")
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  restaurant = relationship("Restaurant", back_populates="orders")
  order_items = relationship("OrderItem", back_populates="order")
  reviews = relationship("Review", back_populates="order")


class OrderItem(Base):
  __tablename__ = "order_items"
  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(Integer, ForeignKey("orders.id"))
  menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
  quantity = Column(Integer, nullable=False)
  order = relationship("Order", back_populates="order_items")


class Review(Base):
  __tablename__ = "reviews"
  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(Integer, ForeignKey("orders.id"))
  rating = Column(Integer, nullable=False)
  comment = Column(Text, nullable=True)
  order = relationship("Order", back_populates="reviews")


class PaymentLedger(Base):
  __tablename__ = "payment_ledger"
  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(Integer, ForeignKey("orders.id"))
  amount = Column(Float, nullable=False)
  status = Column(String, default="SUCCESS")


class AdminReminderLog(Base):
  __tablename__ = "admin_reminder_logs"
  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(Integer, ForeignKey("orders.id"))
  message = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    rating = Column(Integer)
    comment = Column(String)