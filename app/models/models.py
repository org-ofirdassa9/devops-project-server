from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    registration_date = Column(Date, index=True)
    heart_rate = Column(Integer, index=True)
    blood_pressure = Column(String, index=True)
    body_temperature = Column(Float, index=True)
    blood_sugar_level = Column(Float, index=True)
    isAdmin = Column(Boolean, default=False)