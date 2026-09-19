from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///./database.db") # Движок
SessionLocal = sessionmaker(bind=engine) # Класс сессии 
Base = declarative_base() # Класс базового объекта в базе данных

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback() # откат изменений до commit
        raise
    finally:
        db.close()