"""
Populate the database with seed data for food items and exercise items
Usage:
python -m data.populate_db food_items -> populates food_items data
python -m data.populate_db exercise_items -> populates exercise_items data
"""
import sys
import uuid
import json
from pathlib import Path
from app.core.database import get_db
from sqlalchemy.orm import Session
from models.models import FoodItem, ExerciseItem

def insert_food_data(db: Session):

    # Load JSON seed data
    json_path = Path(__file__).parent.parent / "data" / "fooditems.json"
    with open(json_path, "r") as f:  
        food_data = json.load(f)

    # Insert each record into DB
    for item in food_data:
        food_item = FoodItem(
            id=uuid.UUID(item["id"]),
            name=item["name"],
            protein=item["protein"],
            fat=item["fat"],
            carbs=item["carbs"],
            fiber=item["fiber"],
            calories=item["calories"],
            category=item["category"]
        )
        db.add(food_item)

    db.commit()
    db.close()

def insert_exercise_data(db: Session):

    # Load JSON seed data
    json_path = Path(__file__).parent.parent / "data" / "exerciseitems.json"
    with open(json_path, "r") as f:
        exercise_data = json.load(f)

    # Insert each record into DB
    for item in exercise_data:
        exercise_item = ExerciseItem(
            id=uuid.UUID(item["id"]),
            name=item["name"],
            met_value=item["met"],
            category=item["category"]
        )
        db.add(exercise_item)

    db.commit()
    db.close()

def show_usage():
    print(__doc__)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    db = next(get_db())
    if command == "food_items":
        insert_food_data(db)
    elif command == "exercise_items":
        insert_exercise_data(db)
    else:
        print(f"Unknown command: {command}")
        show_usage()
        sys.exit(1)
