import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import validate_email
from app.models.models import User, HealthMetrics
from app.schemas.health_metrics import UserWithFullHealthMetrics
from app.schemas.user_schema import UserInDB, UserUpdate
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me", response_model=UserWithFullHealthMetrics, dependencies=[Depends(HTTPBearer())])
async def read_users_me(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    user = db.query(User).filter(User.email == current_user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch health metrics for the user
    health_metrics = db.query(HealthMetrics).filter(HealthMetrics.user_id == user.user_id).first()

    # Combine User and HealthMetrics data
    user_with_health_metrics = UserWithFullHealthMetrics(
        user_id=user.user_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        heart_rate=health_metrics.heart_rate if health_metrics else None,
        blood_pressure=health_metrics.blood_pressure if health_metrics else None,
        body_temperature=health_metrics.body_temperature if health_metrics else None,
        blood_sugar_level=health_metrics.blood_sugar_level if health_metrics else None,
        min_heart_rate=health_metrics.min_heart_rate if health_metrics else None,
        max_heart_rate=health_metrics.max_heart_rate if health_metrics else None,
        min_blood_pressure=health_metrics.min_blood_pressure if health_metrics else None,
        max_blood_pressure=health_metrics.max_blood_pressure if health_metrics else None,
        min_body_temperature=health_metrics.min_body_temperature if health_metrics else None,
        max_body_temperature=health_metrics.max_body_temperature if health_metrics else None,
        min_blood_sugar_level=health_metrics.min_blood_sugar_level if health_metrics else None,
        max_blood_sugar_level=health_metrics.max_blood_sugar_level if health_metrics else None
    )
    
    return user_with_health_metrics


@router.get("/{user_id}", response_model=UserWithFullHealthMetrics, dependencies=[Depends(HTTPBearer())])
async def read_user_by_id(user_id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    raw_jwt = authorize.get_raw_jwt()
    if not raw_jwt.get("isAdmin"):
        raise HTTPException(status_code=401, detail="Not authorized to update this user")
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch health metrics for the user by user_id
    health_metrics = db.query(HealthMetrics).filter(HealthMetrics.user_id == user_id).first()

    # Combine User and HealthMetrics data
    user_with_health_metrics = UserWithFullHealthMetrics(
        user_id=user.user_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        heart_rate=health_metrics.heart_rate if health_metrics else None,
        blood_pressure=health_metrics.blood_pressure if health_metrics else None,
        body_temperature=health_metrics.body_temperature if health_metrics else None,
        blood_sugar_level=health_metrics.blood_sugar_level if health_metrics else None,
        min_heart_rate=health_metrics.min_heart_rate if health_metrics else None,
        max_heart_rate=health_metrics.max_heart_rate if health_metrics else None,
        min_blood_pressure=health_metrics.min_blood_pressure if health_metrics else None,
        max_blood_pressure=health_metrics.max_blood_pressure if health_metrics else None,
        min_body_temperature=health_metrics.min_body_temperature if health_metrics else None,
        max_body_temperature=health_metrics.max_body_temperature if health_metrics else None,
        min_blood_sugar_level=health_metrics.min_blood_sugar_level if health_metrics else None,
        max_blood_sugar_level=health_metrics.max_blood_sugar_level if health_metrics else None
    )
    
    return user_with_health_metrics

@router.put("/{user_id}", response_model=UserInDB, dependencies=[Depends(HTTPBearer())])
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    if user_id < 1:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    raw_jwt = authorize.get_raw_jwt()
    if current_user != user.email and not raw_jwt.get("isAdmin"):
        raise HTTPException(status_code=401, detail="Not authorized to update this user")

    user_in_db = db.query(User).filter(User.user_id == user_id).first()
    if user_in_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only email, first_name, and last_name if provided
    if user.email:
        validate_email(user.email)
        user_in_db.email = user.email
    if user.first_name:
        user_in_db.first_name = user.first_name
    if user.last_name:
        user_in_db.last_name = user.last_name

    db.commit()
    db.refresh(user_in_db)

    updated_user = UserInDB.from_orm(user_in_db)

    return updated_user
