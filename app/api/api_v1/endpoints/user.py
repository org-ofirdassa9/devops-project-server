from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
import logging
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import UserBase, UserInDB, UserCreate, AccessToken
from app.schemas.login_request import LoginRequest
from app.models.models import User
from app.crud.user_crud import create_user, authenticate_user
from app.core.security import validate_password, validate_email


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/signup", summary="Create new User", response_model=UserInDB)
async def sign_up(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    validate_email(user_create.email)
    validate_password(user_create.password)
    logger.info("Creating new user %s", user_create.email)
    db_user = create_user(db=db, user=user_create)
    # Convert the SQLAlchemy model instance to Pydantic model
    user_response = UserInDB.from_orm(db_user)
    logger.info("User created %s", db_user.email)
    return user_response


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
    return {"message":"The token has been refresh", "access_token": new_access_token}

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
    user_response = UserInDB.from_orm(user)
    logger.info("me: %s", user_response)
    return user_response

@router.get("/{user_id}", response_model=UserInDB, dependencies=[Depends(HTTPBearer())])
async def read_user_by_id(user_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_response = UserInDB.from_orm(user)
    logger.info("UserInDB: %s",user_response)
    return user_response