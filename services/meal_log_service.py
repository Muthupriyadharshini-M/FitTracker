from uuid import UUID
from sqlalchemy.orm import Session
from pydantic import condecimal
from repository.meal_log_repository import MealLogRepository
from repository.food_item_repository import FoodItemRepository
from models.models import MealLog

class MealLogService:
    
    @staticmethod
    def create(db: Session, user_id: str, food_item_id: str, quantity_in_grams: condecimal(gt=0)) -> None:
        # Get and calculate macros
        food_item = FoodItemRepository.get_by_id(db, food_item_id)
        protein = food_item.protein * quantity_in_grams / 100
        fat = food_item.fat * quantity_in_grams / 100   
        carbs = food_item.carbs * quantity_in_grams / 100
        fiber = food_item.fiber * quantity_in_grams / 100
        calories = food_item.calories * quantity_in_grams / 100

        # Create meal log
        meal_log = MealLog(
            user_id=user_id,
            food_item_id=food_item_id,
            quantity_in_grams=quantity_in_grams,
            protein=protein,
            fat=fat,
            carbs=carbs,
            fiber=fiber,
            calories=calories
        )
        return MealLogRepository.create(db, meal_log)
    
    @staticmethod
    def get_all(db: Session, user_id: str):
        return MealLogRepository.get_all(db, user_id)
    
    @staticmethod
    def get_by_id(db: Session, user_id: str, meal_log_id):
        return MealLogRepository.get_by_id(db, user_id, meal_log_id)