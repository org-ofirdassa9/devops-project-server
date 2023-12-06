from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserInDB(UserBase):
    id: int

class UserCreate(UserBase):
    password: str

class AccessToken(BaseModel):
    access_token: str
