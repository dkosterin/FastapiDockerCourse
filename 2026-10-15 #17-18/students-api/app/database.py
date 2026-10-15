from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# Чтобы sqlite работал в асинхроном режиме, нужно установить aiosqlite
# pip install aiosqlite
# sqlite:///./database.db -> sqlite+aiosqlite:///./database.db

# Нужно установить драйвер для работы с postgres
# Синхронный psycopg2 pip install psycopg2-binary
# Асинхронный asyncpg pip install asyncpg

#DATABASE_URL = "sqlite+aiosqlite:///./database.db"
#DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/students_db"
engine = create_async_engine(settings.database_url) # Движок
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