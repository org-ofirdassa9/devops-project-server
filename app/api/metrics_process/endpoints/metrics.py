from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, HealthMetrics
from app.schemas.health_metrics import UserBasicHealthMetrics, UserWithFullHealthMetrics
from fastapi.security import HTTPBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.put("/{user_id}", response_model=UserWithFullHealthMetrics, dependencies=[Depends(HTTPBearer())])
async def update_health_metrics_for_user(user_id: int, user_basic_health_metrics: UserBasicHealthMetrics, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    raw_jwt = authorize.get_raw_jwt()
    user_in_db = db.query(User).filter(User.user_id == user_id).first()
    if user_in_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    email = db.query(User.email).filter(User.user_id == user_id).scalar()
    if current_user_email != email and not raw_jwt.get("isAdmin"):
        raise HTTPException(status_code=401, detail="Not authorized to update this user")
     # Fetch the user's existing health metrics
    user_health_metrics = db.query(HealthMetrics).filter(HealthMetrics.user_id == user_id).first()
    if user_health_metrics is None:
        user_health_metrics = HealthMetrics(user_id=user_id)
        db.add(user_health_metrics)
        db.commit()
        db.refresh(user_health_metrics)
        
    # Update the user's health metrics
    user_health_metrics.heart_rate = user_basic_health_metrics.heart_rate
    user_health_metrics.blood_pressure = user_basic_health_metrics.blood_pressure
    user_health_metrics.body_temperature = user_basic_health_metrics.body_temperature
    user_health_metrics.blood_sugar_level = user_basic_health_metrics.blood_sugar_level
    db.commit()
    db.refresh(user_health_metrics)

    # Check if the new value is bigger or smaller than the min or max value
    if user_health_metrics.min_heart_rate is None or user_health_metrics.heart_rate < user_health_metrics.min_heart_rate:
        user_health_metrics.min_heart_rate = user_health_metrics.heart_rate
        db.commit()
        db.refresh(user_health_metrics)
        
    if user_health_metrics.max_heart_rate is None or user_health_metrics.heart_rate > user_health_metrics.max_heart_rate:
        user_health_metrics.max_heart_rate = user_health_metrics.heart_rate
        db.commit()
        db.refresh(user_health_metrics)
        
    if user_health_metrics.min_blood_pressure is None or user_health_metrics.blood_pressure < user_health_metrics.min_blood_pressure:
        user_health_metrics.min_blood_pressure = user_health_metrics.blood_pressure
        db.commit()
        db.refresh(user_health_metrics)
        
    if user_health_metrics.max_blood_pressure is None or user_health_metrics.blood_pressure > user_health_metrics.max_blood_pressure:
        user_health_metrics.max_blood_pressure = user_health_metrics.blood_pressure
        db.commit()
        db.refresh(user_health_metrics)
        
    if user_health_metrics.min_body_temperature is None or user_health_metrics.body_temperature < user_health_metrics.min_body_temperature:
        user_health_metrics.min_body_temperature = user_health_metrics.body_temperature
        db.commit()
        db.refresh(user_health_metrics)
        
    if user_health_metrics.max_body_temperature is None or user_health_metrics.body_temperature > user_health_metrics.max_body_temperature:
        user_health_metrics.max_body_temperature = user_health_metrics.body_temperature
        db.commit()
        db.refresh(user_health_metrics)
        
    if user_health_metrics.min_blood_sugar_level is None or user_health_metrics.blood_sugar_level < user_health_metrics.min_blood_sugar_level:
        user_health_metrics.min_blood_sugar_level = user_health_metrics.blood_sugar_level
        db.commit()
        db.refresh(user_health_metrics)
        
    if user_health_metrics.max_blood_sugar_level is None or user_health_metrics.blood_sugar_level > user_health_metrics.max_blood_sugar_level:
        user_health_metrics.max_blood_sugar_level = user_health_metrics.blood_sugar_level
        db.commit()
        db.refresh(user_health_metrics)
        
    # Return the updated user with health metrics
    updated_user_with_health_metrics = UserWithFullHealthMetrics(
        user_id=user_in_db.user_id,
        email=user_in_db.email,
        first_name=user_in_db.first_name,
        last_name=user_in_db.last_name,
        heart_rate=user_health_metrics.heart_rate,
        blood_pressure=user_health_metrics.blood_pressure,
        body_temperature=user_health_metrics.body_temperature,
        blood_sugar_level=user_health_metrics.blood_sugar_level,
        min_heart_rate=user_health_metrics.min_heart_rate,
        max_heart_rate=user_health_metrics.max_heart_rate,
        min_blood_pressure=user_health_metrics.min_blood_pressure,
        max_blood_pressure=user_health_metrics.max_blood_pressure,
        min_body_temperature=user_health_metrics.min_body_temperature,
        max_body_temperature=user_health_metrics.max_body_temperature,
        min_blood_sugar_level=user_health_metrics.min_blood_sugar_level,
        max_blood_sugar_level=user_health_metrics.max_blood_sugar_level
        )
    return updated_user_with_health_metrics