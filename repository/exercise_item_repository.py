from sqlalchemy.orm import Session
from models.models import ExerciseItem

class ExerciseItemRepository:

    @staticmethod
    def get_by_id(db: Session, exercise_item_id: str):
        return db.query(ExerciseItem).filter(ExerciseItem.id == exercise_item_id).first()
