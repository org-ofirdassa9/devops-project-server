from pydantic import BaseModel

# Shared properties
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str