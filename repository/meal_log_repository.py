from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from models.models import MealLog, FoodItem

class MealLogRepository:

    @staticmethod
    def create(db: Session, meal_log: MealLog):
        db.add(meal_log)
        db.commit()
        db.refresh(meal_log)
        return meal_log
    
    @staticmethod
    def get_all(db: Session, user_id: UUID):
        query = db.query(MealLog).filter(MealLog.user_id == user_id)
        query = query.options(
            joinedload(MealLog.food_item).load_only(FoodItem.id, FoodItem.name)
        )
        meal_logs = query.all()
        return meal_logs
    
    @staticmethod
    def get_by_id(db: Session, user_id: UUID, meal_log_id: UUID):
        query = db.query(MealLog).filter(MealLog.user_id == user_id, MealLog.id == meal_log_id)
        query = query.options(
            joinedload(MealLog.food_item).load_only(FoodItem.id, FoodItem.name)
        )
        meal_logs = query.all()
        if not len(meal_logs):
            raise ValueError('Meal log wasn\'t found')

        return meal_logs[0]
    
    @staticmethod
    def update(db: Session, meal_log: MealLog):
        db.commit()
        db.refresh(meal_log)
        return meal_log

    @staticmethod
    def delete(db: Session, user_id: UUID, meal_log_id: UUID):
        result = db.query(MealLog).filter(
            MealLog.id == meal_log_id,
            MealLog.user_id == user_id
        ).delete()
        
        db.commit()


    