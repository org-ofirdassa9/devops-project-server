from sqlalchemy.orm import Session
from app.models.models import User, HealthMetrics
from app.schemas.user_schema import UserCreate, UserInDB
from app.core.security import get_hashed_password, verify_password
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate) -> UserInDB:
    hashed_password = get_hashed_password(user.password)
    
    # Create User instance
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        registration_date=datetime.now(),
        isAdmin=False
    )
    
    # Commit User to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create HealthMetrics entry for the new user with default values
    db_health_metrics = HealthMetrics(
        user_id=db_user.user_id,
        heart_rate=0,  # Set default values as needed
        blood_pressure=0.0,
        body_temperature=0.0,
        blood_sugar_level=0.0,
        min_heart_rate=0,
        max_heart_rate=0,
        min_blood_pressure=0.0,
        max_blood_pressure=0.0,
        min_body_temperature=0.0,
        max_body_temperature=0.0,
        min_blood_sugar_level=0.0,
        max_blood_sugar_level=0.0
    )
    
    # Commit HealthMetrics entry for the new user
    db.add(db_health_metrics)
    db.commit()
    
    return UserInDB.from_orm(db_user)

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return UserInDB.from_orm(user)
