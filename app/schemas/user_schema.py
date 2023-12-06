from pydantic import BaseModel

# Shared properties
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    address: str = None
    phone_number: str = None
    marketing_allowed: bool
    profile_image: str = None

# Properties to receive on user update
class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True

# Properties to receive on user creation
class UserCreate(UserBase):
    password: str

# Properties to return to client
class AccessToken(BaseModel):
    access_token: str
