from typing import Optional
from pydantic import BaseModel, condecimal
from uuid import UUID
from datetime import datetime

# These are schema associated with API requests
class UserCreateIn(BaseModel):
    username: str
    email: str
    password: str

class CreateOut(BaseModel):
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

class MealLogCreateIn(BaseModel):
    food_item_id: UUID  
    quantity_in_grams: int
    consumed_at: Optional[datetime] = None

class FoodItemOut(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
    

class MealLogGetOut(BaseModel):
    id: UUID
    quantity_in_grams: int
    consumed_at: datetime 
    created_at: datetime
    updated_at: Optional[datetime] = None 
    protein: condecimal(gt=-1)
    fiber:  condecimal(gt=-1)
    carbs: condecimal(gt=-1)
    calories: condecimal(gt=-1)
    fat: condecimal(gt=-1)
    food_item: FoodItemOut

    class Config:
        orm_mode = True

class MealLogsGetOut(BaseModel):
    meal_logs: list[MealLogGetOut]

    class Config:
        orm_mode = True