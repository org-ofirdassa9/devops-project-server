import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.user_schema import UserInDB
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
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_response = UserInDB.from_orm(user)
    logger.info("UserInDB: %s", user_response)
    return user_response