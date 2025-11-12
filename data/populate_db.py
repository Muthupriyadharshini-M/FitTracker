import uuid
import json
from pathlib import Path
from app.core.database import get_db
from sqlalchemy.orm import Session
from models.models import FoodItem

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


if __name__ == "__main__":
    db = next(get_db())
    insert_food_data(db)