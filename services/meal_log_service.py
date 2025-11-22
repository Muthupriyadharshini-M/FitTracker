import datetime
from sqlalchemy.orm import Session
from pydantic import condecimal
from repository.meal_log_repository import MealLogRepository
from repository.food_item_repository import FoodItemRepository
from models.models import MealLog

class MealLogService:

    @staticmethod
    def _calculate_macros(food_item, quantity_in_grams):
        protein = food_item.protein * quantity_in_grams / 100
        fat = food_item.fat * quantity_in_grams / 100
        carbs = food_item.carbs * quantity_in_grams / 100
        fiber = food_item.fiber * quantity_in_grams / 100
        calories = food_item.calories * quantity_in_grams / 100
        return protein, fat, carbs, fiber, calories
    
    @staticmethod
    def create(db: Session, user_id: str, food_item_id: str, quantity_in_grams: condecimal(gt=0), consumed_at: datetime) -> None:
        # Get and calculate macros
        food_item = FoodItemRepository.get_by_id(db, food_item_id)
        if not food_item:
            raise ValueError("Food item not found")
        
        protein, fat, carbs, fiber, calories = MealLogService._calculate_macros(food_item, quantity_in_grams)

        # Create meal log
        meal_log = MealLog(
            user_id=user_id,
            food_item_id=food_item_id,
            quantity_in_grams=quantity_in_grams,
            protein=protein,
            fat=fat,
            carbs=carbs,
            fiber=fiber,
            calories=calories,
            consumed_at=consumed_at
        )
        return MealLogRepository.create(db, meal_log)
    
    @staticmethod
    def get_all(db: Session, user_id: str):
        return MealLogRepository.get_all(db, user_id)
    
    @staticmethod
    def get_by_id(db: Session, user_id: str, meal_log_id):
        return MealLogRepository.get_by_id(db, user_id, meal_log_id)
    
    @staticmethod
    def update(db: Session, user_id: str, meal_log_id: str, food_item_id: str, quantity_in_grams: condecimal(gt=0), consumed_at: datetime):
        
        # Verify the meal log exists and belongs to the user
        existing_meal_log = MealLogRepository.get_by_id(db, user_id, meal_log_id)
        if not existing_meal_log:
            raise ValueError("Meal log not found")
        
        # Get food item and recalculate macros
        food_item = FoodItemRepository.get_by_id(db, food_item_id)
        if not food_item:
            raise ValueError("Food item not found")
        
        # Calculate new macros
        existing_meal_log.food_item_id = food_item_id
        existing_meal_log.quantity_in_grams = quantity_in_grams
        existing_meal_log.protein, existing_meal_log.fat, existing_meal_log.carbs, existing_meal_log.fiber, existing_meal_log.calories = MealLogService._calculate_macros(food_item, quantity_in_grams)
        existing_meal_log.consumed_at = consumed_at
        
        # Use repository to persist changes
        return MealLogRepository.update(db, existing_meal_log)
    
    @staticmethod
    def delete(db: Session, user_id: str, meal_log_id: str):
        existing_meal_log = MealLogRepository.get_by_id(db, user_id, meal_log_id)
        if not existing_meal_log:
            raise ValueError("Meal log not found")
        meal_log = MealLogRepository.delete(db, user_id, meal_log_id)
