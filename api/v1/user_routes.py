from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, Request
from app.core.database import get_db
from services.user_service import UserService
from utils.security import create_access_token, get_current_user
from schema.schema import UserCreateUpdateIn, CreateUpdateDeleteOut, UserLogin, UserLoginOut, GetUserOut

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=CreateUpdateDeleteOut)
def register_user(user_in: UserCreateUpdateIn, db: Session = Depends(get_db)):
    try:
        user = UserService.register(db, user_in.username, user_in.email, user_in.password, user_in.weight_in_kg)
        return {"success": True, "id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserLoginOut)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    try:
        user = UserService.authenticate(db, user_in.email, user_in.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    access_token = create_access_token(str(user.id))
    return {"success": True, "id": user.id, "access_token": access_token, "token_type": "bearer"}

@router.patch("/user", response_model=CreateUpdateDeleteOut)
def update_user(user_in: UserCreateUpdateIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = get_current_user(token)
        user = UserService.update(db, user_id, user_in.username, user_in.email, user_in.password, user_in.weight_in_kg)
        return {"success": True, "id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user", response_model=GetUserOut)
def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try: 
        user_id = get_current_user(token)
        user = UserService.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})

@router.delete("/user", response_model=CreateUpdateDeleteOut)
def delete_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try: 
        user_id = get_current_user(token)
        UserService.delete(db, user_id)
        return {"success": True, "id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    
