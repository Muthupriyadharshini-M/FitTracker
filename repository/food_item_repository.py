from uuid import UUID
from sqlalchemy.orm import Session
from models.models import FoodItem

class FoodItemRepository:

    @staticmethod
    def get_by_id(db: Session, food_item_id: str):
        return db.query(FoodItem).filter(FoodItem.id == food_item_id).first()
