from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    registration_date = Column(Date)
    isAdmin = Column(Boolean, default=False)

    health_metrics = relationship("HealthMetrics", back_populates="user")

#saves the current, min and max values of the health metrics of the users.
class HealthMetrics(Base):
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    heart_rate = Column(Integer, index=True)
    blood_pressure = Column(String, index=True)
    body_temperature = Column(Float, index=True)
    blood_sugar_level = Column(Float, index=True)
    min_heart_rate = Column(Integer, index=True)
    max_heart_rate = Column(Integer, index=True)
    min_blood_pressure = Column(String, index=True)
    max_blood_pressure = Column(String, index=True)
    min_body_temperature = Column(Float, index=True)
    max_body_temperature = Column(Float, index=True)
    min_blood_sugar_level = Column(Float, index=True)
    max_blood_sugar_level = Column(Float, index=True)
    
    user = relationship("User", back_populates="health_metrics")