from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from models.models import ExerciseItem, ExerciseLog

class ExerciseLogRepository:

    @staticmethod
    def create(db: Session, exercise_log: ExerciseLog):
        db.add(exercise_log)
        db.commit()
        db.refresh(exercise_log)
        return exercise_log
    
    @staticmethod
    def get_all(db: Session, user_id: UUID):
        query = db.query(ExerciseLog).filter(ExerciseLog.user_id == user_id)
        query = query.options(
            joinedload(ExerciseLog.exercise_item).load_only(ExerciseItem.id, ExerciseItem.name)
        )
        exercise_logs = query.all()
        return exercise_logs
    
    @staticmethod
    def get_by_id(db: Session, user_id: UUID, exercise_log_id: UUID):
        query = db.query(ExerciseLog).filter(ExerciseLog.user_id == user_id, ExerciseLog.id == exercise_log_id)
        query = query.options(
            joinedload(ExerciseLog.exercise_item).load_only(ExerciseItem.id, ExerciseItem.name)
        )
        exercise_logs = query.all()
        if not len(exercise_logs):
            raise ValueError('Exercise log wasn\'t found')

        return exercise_logs[0]
    
    @staticmethod
    def update(db: Session, exercise_log: ExerciseLog):
        db.commit()
        db.refresh(exercise_log)
        return exercise_log

    @staticmethod
    def delete(db: Session, user_id: UUID, exercise_log_id: UUID):
        result = db.query(ExerciseLog).filter(
            ExerciseLog.id == exercise_log_id,
            ExerciseLog.user_id == user_id
        ).delete()
        
        db.commit()


    