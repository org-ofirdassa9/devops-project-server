from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.user_schema import UserCreate, UserInDB
from app.core.security import get_hashed_password, verify_password
import logging

logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    user_dict = user.dict()
    user_dict.pop('password')
    db_user = User(**{**user_dict, 'hashed_password': hashed_password})
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
