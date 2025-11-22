from typing import Optional
from pydantic import BaseModel, condecimal
from uuid import UUID
from datetime import datetime

# These are schema associated with API requests
class UserCreateUpdateIn(BaseModel):
    username: str
    email: str
    password: str
    weight_in_kg: float

class CreateUpdateDeleteOut(BaseModel):
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

class MealLogCreateUpdateIn(BaseModel):
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

class ExerciseLogCreateUpdateIn(BaseModel):
    exercise_item_id: UUID
    duration_in_minutes: int
    performed_at: Optional[datetime] = None

class ExerciseItemOut(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
    
class ExerciseLogGetOut(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None 
    duration_in_minutes: int
    calories_burned: condecimal(gt=-1)
    exercise_item: ExerciseItemOut

    class Config:
        orm_mode = True

class ExerciseLogsGetOut(BaseModel):
    exercise_logs: list[ExerciseLogGetOut]

    class Config:
        orm_mode = True