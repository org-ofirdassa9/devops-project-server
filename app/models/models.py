from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    address = Column(String, index=True, nullable=True)
    profile_image = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    marketing_allowed = Column(Boolean, index=True)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), index=True)
    category = Column(Integer, ForeignKey('categories.id'), index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    price_per_day = Column(Integer, index=True)
    availability_status = Column(Boolean, index=True)

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    equipment_id = Column(Integer, ForeignKey('equipments.id'), index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    payment_status = Column(Boolean, index=True)
    price = Column(Integer, index=True)
    payment_method = Column(String, index=True)
    transaction_id = Column(String, index=True, nullable=True)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    equipment_id = Column(Integer, ForeignKey('equipments.id'), index=True)
    rating = Column(Integer, index=True)
    comment = Column(String, nullable=True)
    created_at = Column(Date, index=True)
    updated_at = Column(Date, index=True)