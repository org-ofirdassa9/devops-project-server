import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import validate_email
from app.models.models import User
from app.schemas.user_schema import UserInDB, UserUpdate
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me", response_model=UserInDB, dependencies=[Depends(HTTPBearer())])
async def read_users_me(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    user = db.query(User).filter(User.email == current_user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_response = UserInDB.from_orm(user)
    logger.info("me: %s", user_response)
    return user_response


@router.get("/{user_id}", response_model=UserInDB, dependencies=[Depends(HTTPBearer())])
async def read_user_by_id(user_id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    raw_jwt = authorize.get_raw_jwt()
    if not raw_jwt.get("isAdmin"):
        raise HTTPException(status_code=401, detail="Not authorized to update this user")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_response = UserInDB.from_orm(user)
    logger.info("UserInDB: %s", user_response)
    return user_response


@router.put("/{user_id}", response_model=UserInDB, dependencies=[Depends(HTTPBearer())])
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    raw_jwt = authorize.get_raw_jwt()
    if current_user != user.email and not raw_jwt.get("isAdmin"):
        logger.info("current_user: %s", current_user)
        logger.info("user.email: %s", user.email)
        raise HTTPException(status_code=401, detail="Not authorized to update this user")
    user_in_db = db.query(User).filter(User.id == user_id).first()
    if user_in_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.email is not None and user.email != user_in_db.email:
        validate_email(user.email)
    for field, value in user.dict(exclude_unset=True).items():
        setattr(user_in_db, field, value)
    db.commit()
    db.refresh(user_in_db)
    user_response = UserInDB.from_orm(user_in_db)
    logger.info("user_response: %s", user_response)
    return user_response