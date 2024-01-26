from typing import Optional
from pydantic import BaseModel

from app.schemas.user_schema import UserBase

class UserBasicHealthMetrics(BaseModel):
    heart_rate: Optional[int]
    blood_pressure: Optional[float]
    body_temperature: Optional[float]
    blood_sugar_level: Optional[float]


class UserWithFullHealthMetrics(UserBase):
    user_id: int
    heart_rate: int
    blood_pressure: float
    body_temperature: float
    blood_sugar_level: float
    min_heart_rate: int
    max_heart_rate: int
    min_blood_pressure: float
    max_blood_pressure: float
    min_body_temperature: float
    max_body_temperature: float
    min_blood_sugar_level: float
    max_blood_sugar_level: float

    class Config:
        orm_mode = True