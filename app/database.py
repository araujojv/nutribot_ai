from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os
from sqlalchemy.orm import Session

os.makedirs("data", exist_ok=True)

DATABASE_URL = "sqlite:///data/nutricao.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()