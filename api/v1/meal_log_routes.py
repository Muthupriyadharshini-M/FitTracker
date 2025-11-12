from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from utils.security import get_current_user
from services.meal_log_service import MealLogService
from schemas.schema import MealLogCreateIn, CreateOut, MealLogsGetOut, MealLogGetOut
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/meal_log", response_model=CreateOut)
def create_meal_log(meal_log_in: MealLogCreateIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        meal_log = MealLogService.create(db, user_id, meal_log_in.food_item_id, meal_log_in.quantity_in_grams)
        return {"success": True, "id": meal_log.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/meal_logs", response_model=MealLogsGetOut)
def get_meal_logs(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        meal_logs = MealLogService.get_all(db, user_id)
        return {"meal_logs": meal_logs}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/meal_log/{meal_log_id}", response_model=MealLogGetOut)
def get_meal_logs(meal_log_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        meal_log = MealLogService.get_by_id(db, user_id, meal_log_id)
        return meal_log
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))