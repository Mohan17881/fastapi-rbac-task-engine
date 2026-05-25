from pydantic import BaseModel,EmailStr
from datetime import datetime



class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True            