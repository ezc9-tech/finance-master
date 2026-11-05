import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///example.db")
engine = create_engine(DATABASE_URL, echo=True)
localSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()
