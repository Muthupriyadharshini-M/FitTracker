"""
Migration: Update users table's schema
Usage:
  python migrations/user_schema_migration.py add_weight_optional    - Add 'weight' field as optional
  python migrations/user_schema_migration.py make_weight_required   - Make 'weight' field mandatory
  python migrations/user_schema_migration.py remove_weight          - Remove 'weight' field
"""

import sys
from sqlalchemy import text
from app.core.database import db_instance

def add_optional():
    with db_instance.engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS weight FLOAT
        """))
        conn.commit()

def make_required():
    with db_instance.engine.connect() as conn:
        
        # Check if any users still have NULL weight
        result = conn.execute(text("""
            SELECT COUNT(*) FROM users WHERE weight IS NULL
        """))
        null_count = result.scalar()
        
        if null_count > 0:
            print(f"Cannot proceed! {null_count} users still have NULL weight.")
            return
        conn.execute(text("""
            ALTER TABLE users 
            ALTER COLUMN weight SET NOT NULL
        """))
        
        conn.commit()

def remove():
    
    with db_instance.engine.connect() as conn:
        
        conn.execute(text("""
            ALTER TABLE users 
            DROP COLUMN IF EXISTS weight
        """))
        conn.commit()

def show_usage():
    print(__doc__)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add_weight_optional":
        add_optional()
    elif command == "make_weight_required":
        make_required()
    elif command == "remove_weight":
        remove()
    else:
        print(f"Unknown command: {command}")
        show_usage()
        sys.exit(1)
