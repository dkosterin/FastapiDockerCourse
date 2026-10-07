from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Чтобы sqlite работал в асинхроном режиме, нужно установить aiosqlite
# pip install aiosqlite
# sqlite:///./database.db -> sqlite+aiosqlite:///./database.db

engine = create_async_engine("sqlite+aiosqlite:///./database.db") # Движок
AsyncSessionLocal = async_sessionmaker(bind=engine) # Класс сессии 
Base = declarative_base() # Класс базового объекта в базе данных

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    except Exception:
        await db.rollback() # откат изменений до commit
        raise
    finally:
        await db.close()