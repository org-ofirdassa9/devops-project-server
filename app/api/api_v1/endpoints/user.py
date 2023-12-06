from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
import logging
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import UserBase, UserInDB, UserCreate, AccessToken
from app.schemas.login_request import LoginRequest
from app.models.user_model import User
from app.crud.user_crud import create_user, authenticate_user
from app.core.security import validate_password, validate_email


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/signup", summary="Create new User", response_model=UserInDB)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    validate_password(user.password)
    validate_email(user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_user = create_user(db=db, user=user)
    new_user = UserInDB(email=db_user.email,id=db_user.id)
    logger.info("%s successfully signed up", new_user)
    return new_user


@router.post("/login", summary="Create access and refresh tokens for user", response_model=AccessToken)
async def login(login_request: LoginRequest, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    # Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    token=AccessToken(access_token=access_token)
    logger.info("%s signed in", login_request.email)
    return token

@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}

@router.post('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Log the user out by clearing the HTTP-only cookies.
    """
    logger.info("Clearing cookies")
    Authorize.unset_jwt_cookies()
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserInDB, dependencies=[Depends(HTTPBearer())])
async def read_users_me(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.email == current_user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    me = UserInDB(email=user.email,id=user.id)
    logger.info("me: %s", me)
    return me

@router.get("/{user_id}", response_model=UserInDB, dependencies=[Depends(HTTPBearer())])
async def read_user_by_id(user_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_response = UserInDB(email=user.email,id=user.id)
    logger.info("UserInDB: %s",user_response)
    return user_response