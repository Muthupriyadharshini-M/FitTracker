from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# These are schemas associated with API requests

class UserCreateIn(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    success: bool
    id: UUID

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginOut(BaseModel):
    success: bool
    id: UUID
    access_token: str
    token_type: str

class GetUserOut(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


