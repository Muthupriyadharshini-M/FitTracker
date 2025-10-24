from uuid import UUID
from sqlalchemy.orm import Session
from models.users_model import User

class UserRepository:
    
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: UUID):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user_id: UUID):
        db.query(User).filter(User.id == user_id).delete()
        db.commit()
        return True
