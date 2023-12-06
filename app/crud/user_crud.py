from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserInDB
from app.core.security import get_hashed_password, verify_password

def create_user(db: Session, user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> UserInDB:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return UserInDB(id=user.id,email=user.email)
