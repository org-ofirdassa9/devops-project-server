from typing import Optional
from pydantic import BaseModel
from datetime import date

# Shared properties
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
        
# Properties to receive on user update
class UserInDB(UserBase):
    user_id: int
    registration_date: date
    isAdmin: bool

    class Config:
        orm_mode = True

# Properties to receive on user creation
class UserCreate(UserBase):
    password: str

#Updating user information
class UserUpdate(BaseModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        orm_mode = True

# Properties to return to client
class AccessToken(BaseModel):
    access_token: str
