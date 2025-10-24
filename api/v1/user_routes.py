from uuid import UUID
from sqlalchemy.orm import Session
from app.core.database import get_db
from services.user_service import UserService
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, Request
from utils.security import create_access_token, verify_user_access
from schemas.user_schema import UserCreateIn, UserOut, UserLogin, UserLoginOut, GetUserOut

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=UserOut)
def register_user(user_in: UserCreateIn, db: Session = Depends(get_db)):
    try:
        user = UserService.register(db, user_in.username, user_in.email, user_in.password)
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

@router.get("/get_user/{user_id}", response_model=GetUserOut)
def get_user(user_id: UUID, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try: 
        verify_user_access(token, user_id)
        user = UserService.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})

@router.delete("/delete_user/{user_id}", response_model=UserOut)
def get_user(user_id: UUID, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try: 
        verify_user_access(token, user_id)
        UserService.delete(db, user_id)
        return {"success": True, "id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    
