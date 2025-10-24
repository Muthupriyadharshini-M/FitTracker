# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

class Database:
    def __init__(self):
        DB_USER = os.getenv("DB_USER")
        DB_PASS = os.getenv("DB_PASS")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", 5432)
        DB_NAME = os.getenv("DB_NAME")

        DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        self.engine = create_engine(
            DATABASE_URL,
            echo=True,
            pool_size=5,
            max_overflow=10
        )
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.base = declarative_base()
        self.engine = create_engine(DATABASE_URL, echo=True)

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()


# Create a single shared instance
db_instance = Database()
get_db = db_instance.get_db
base = db_instance.base
