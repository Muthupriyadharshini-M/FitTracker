import uuid
from sqlalchemy import Column, String, DateTime, Float, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func
from app.core.database import db_instance, base

# These are DB table models used to create tables and to insert records
class User(base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    meal_logs = relationship("MealLog", back_populates="user", cascade="all, delete-orphan")
    exercise_logs = relationship("ExerciseLog", back_populates="user", cascade="all, delete-orphan")

class FoodItem(base):
    __tablename__ = "food_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fiber = Column(Float, nullable=False)
    calories = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    meal_logs = relationship("MealLog", back_populates="food_item")

class MealLog(base):
    __tablename__ = "meal_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    food_item_id = Column(UUID(as_uuid=True), ForeignKey("food_items.id"), nullable=False)
    quantity_in_grams = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fiber = Column(Float, nullable=False)
    calories = Column(Float, nullable=False)
    consumed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="meal_logs")
    food_item = relationship("FoodItem", back_populates="meal_logs")

class ExerciseItem(base):
    __tablename__ = "exercise_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    met_value = Column(Numeric(4, 2), nullable=False)
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    exercise_logs = relationship("ExerciseLog", back_populates="exercise_item")

class ExerciseLog(base):
    __tablename__ = "exercise_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exercise_item_id = Column(UUID(as_uuid=True), ForeignKey("exercise_items.id"), nullable=False)

    duration_in_minutes = Column(Numeric(10, 2), nullable=False)
    calories_burned = Column(Numeric(10, 2), nullable=False)  

    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="exercise_logs")
    exercise_item = relationship("ExerciseItem", back_populates="exercise_logs")

if __name__ == "__main__":
    db_instance.base.metadata.create_all(bind=db_instance.engine)

    
