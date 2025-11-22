from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from utils.security import get_current_user
from services.exercise_log_service import ExercieLogService
from schema.schema import ExerciseLogCreateUpdateIn, CreateUpdateDeleteOut, ExerciseLogsGetOut, ExerciseLogGetOut
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/exercise_log", response_model=CreateUpdateDeleteOut)
def create_exercise_log(exercise_log_in: ExerciseLogCreateUpdateIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        exercise_log = ExercieLogService.create(db, user_id, exercise_log_in.exercise_item_id, exercise_log_in.duration_in_minutes, exercise_log_in.performed_at)
        return {"success": True, "id": exercise_log.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/exercise_log/{exercise_log_id}", response_model=CreateUpdateDeleteOut)
def update_exercise_log(exercise_log_id: str, exercise_log_in: ExerciseLogCreateUpdateIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        exercise_log = ExercieLogService.update(db, user_id, exercise_log_id, exercise_log_in.exercise_item_id, exercise_log_in.duration_in_minutes, exercise_log_in.performed_at)
        return {"success": True, "id": exercise_log.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/exercise_logs", response_model=ExerciseLogsGetOut)
def get_exercise_logs(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        exercise_logs = ExercieLogService.get_all(db, user_id)
        return {"exercise_logs": exercise_logs}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/exercise_log/{exercise_log_id}", response_model=ExerciseLogGetOut)
def get_exercise_log(exercise_log_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        exercise_log = ExercieLogService.get_by_id(db, user_id, exercise_log_id)
        return exercise_log
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/exercise_log/{exercise_log_id}", response_model=CreateUpdateDeleteOut)
def delete_exercise_log(exercise_log_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        ExercieLogService.delete(db, user_id, exercise_log_id)
        return {"success": True, "id": exercise_log_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))