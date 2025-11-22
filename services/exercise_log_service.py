import datetime
from sqlalchemy.orm import Session
from pydantic import condecimal
from repository.user_repository import UserRepository
from repository.exercise_item_repository import ExerciseItemRepository
from repository.exercise_log_repository import ExerciseLogRepository
from models.models import ExerciseLog

class ExercieLogService:

    @staticmethod
    def _calculate_calories_burned(exercise_item, duration_in_minutes, user):
        calories_burned = float(exercise_item.met_value) * user.weight * (duration_in_minutes / 60)
        return calories_burned
    
    @staticmethod
    def create(db: Session, user_id: str, exercise_item_id: str, duration_in_minutes: condecimal(gt=0), performed_at: datetime) -> None:
        # Get and calculate calories burned
        exercise_item = ExerciseItemRepository.get_by_id(db, exercise_item_id)
        if not exercise_item:
            raise ValueError("Exercise item not found")
        
        user =  UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        calories_burned = ExercieLogService._calculate_calories_burned(exercise_item, duration_in_minutes, user)

        # Create exercise log
        exercise_log = ExerciseLog(
            user_id=user_id,
            exercise_item_id=exercise_item_id,
            duration_in_minutes=duration_in_minutes,
            calories_burned=calories_burned,
            performed_at=performed_at
        )
        
        return ExerciseLogRepository.create(db, exercise_log)
    
    @staticmethod
    def get_all(db: Session, user_id: str):
        return ExerciseLogRepository.get_all(db, user_id)
    
    @staticmethod
    def get_by_id(db: Session, user_id: str, exercise_log_id):
        return ExerciseLogRepository.get_by_id(db, user_id, exercise_log_id)
    
    @staticmethod
    def update(db: Session, user_id: str, exercise_log_id: str, exercise_item_id: str, duration_in_minutes: condecimal(gt=0), performed_at: datetime):
        
        # Verify the exercise log exists and belongs to the user
        existing_exercise_log = ExerciseLogRepository.get_by_id(db, user_id, exercise_log_id)
        if not existing_exercise_log:
            raise ValueError("Exercise log not found")
        
        # Get exercise item and recalculate calories burned
        exercise_item = ExerciseItemRepository.get_by_id(db, exercise_item_id)
        if not exercise_item:
            raise ValueError("Exercise item not found")
        
        # Update fields
        existing_exercise_log.exercise_item_id = exercise_item_id
        existing_exercise_log.duration_in_minutes = duration_in_minutes
        existing_exercise_log.calories_burned = ExercieLogService._calculate_calories_burned(exercise_item, duration_in_minutes, existing_exercise_log.user)
        existing_exercise_log.performed_at = performed_at
        
        # Use repository to persist changes
        return ExerciseLogRepository.update(db, existing_exercise_log)
    
    @staticmethod
    def delete(db: Session, user_id: str, exercise_log_id: str):
        existing_exercise_log = ExerciseLogRepository.get_by_id(db, user_id, exercise_log_id)
        if not existing_exercise_log:
            raise ValueError("Exercise log not found")
        exercise_log = ExerciseLogRepository.delete(db, user_id, exercise_log_id)
        return exercise_log