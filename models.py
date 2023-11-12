from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(500))
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inventory = relationship("Inventory", back_populates="product")
    category = relationship("Category", back_populates="product")
    sale = relationship("Sale", back_populates="product")

    # Foreign key
    category_id = Column(Integer, ForeignKey("category.id"))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    product = relationship("Product", back_populates="category")
    inventory = relationship("Inventory", back_populates="category")
    sale = relationship("Sale", back_populates="category")
    revenue = relationship("Revenue", back_populates="category")


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key relationship
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="inventory")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="inventory")


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Integer) #sales = total no of items ( quantity ) * actual price
    quantity = Column(Integer, default=0) 

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

     # Foreign key relationship
    product_id = Column(Integer, ForeignKey("product.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    product = relationship("Product", back_populates="sale")
    category = relationship("Category", back_populates="sale")
    revenue = relationship("Revenue", back_populates="sale")

class Revenue(Base):
    __tablename__ = 'revenue'

    id = Column(Integer, primary_key=True, index=True)
    revenueSales = Column(Integer) #revenue = total sales + other source of income
    revenueOtherActivities = Column(Integer)
    revenue = Column(Integer) # revenueSales + revenueOtherActivities

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

     # Foreign key relationship
    sale_id = Column(Integer, ForeignKey("sale.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    sale = relationship("Sale", back_populates="revenue")
    category = relationship("Category", back_populates="revenue")   


