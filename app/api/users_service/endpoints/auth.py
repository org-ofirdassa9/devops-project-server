from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import UserInDB, UserCreate, AccessToken
from app.schemas.login_request import LoginRequest
from app.models.models import User
from app.crud.user_crud import create_user, authenticate_user
from app.core.security import validate_password, validate_email
import logging

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
    user_response = UserInDB.from_orm(db_user)
    logger.info("User created %s", user_response)
    return user_response


@router.post("/login", summary="Create access and refresh tokens for user", response_model=AccessToken)
async def login(login_request: LoginRequest, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    claims = {"isAdmin": user.isAdmin}
    access_token = authorize.create_access_token(subject=user.email, user_claims=claims)
    refresh_token = authorize.create_refresh_token(subject=user.email, user_claims=claims)
    authorize.set_refresh_cookies(refresh_token)
    token = AccessToken(access_token=access_token)
    logger.info("%s signed in", login_request.email)
    return token


@router.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    raw_jwt = authorize.get_raw_jwt()
    claims = {"isAdmin": raw_jwt.get("isAdmin")}
    new_access_token = authorize.create_access_token(subject=current_user, user_claims=claims)
    # Set the JWT and CSRF double submit cookies in the response
    authorize.set_access_cookies(new_access_token)
    return {"message": "The token has been refresh", "access_token": new_access_token}


@router.post('/logout')
def logout(authorize: AuthJWT = Depends()):
    """
    Log the user out by clearing the HTTP-only cookies.
    """
    logger.info("Clearing cookies")
    authorize.unset_jwt_cookies()
    return {"message": "Logged out successfully"}
