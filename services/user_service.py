from uuid import UUID
from sqlalchemy.orm import Session
from models.models import User
from utils.security import hash_password, verify_password
from repository.user_repository import UserRepository

class UserService:
    
    @staticmethod
    def register(db: Session, username: str, email: str, password: str) -> None:
        # Check if email already exists
        if UserService.get_by_email(db, email):
            raise ValueError("Email already registered")
        
        hashed_password = hash_password(password)
        user = User(username=username, email=email, hashed_password=hashed_password)
        user = UserRepository.create(db, user)
        return user
    
    @staticmethod
    def authenticate(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)
        
        if not user or not verify_password(password, user.hashed_password):
            return ValueError("Invalid email or password")
        
        return user
    
    @staticmethod
    def get_by_id(db: Session, user_id: UUID):
        return UserRepository.get_by_id(db, user_id)
    
    @staticmethod
    def get_by_email(db: Session, email: str):
        return UserRepository.get_by_email(db, email)
    
    @staticmethod
    def delete(db: Session, user_id: UUID):
        UserRepository.delete(db, user_id)

    
