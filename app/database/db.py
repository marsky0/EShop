from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase 
from functools import wraps

from app.core.config import settings

#SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database.db"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}"

class Base(DeclarativeBase):
    pass

engine: AsyncEngine = None 
session_maker: AsyncSession = None 

async def init_db():
    global engine, session_maker
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    session_maker = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return (engine, session_maker)

async def get_session():
    async with session_maker() as s:
        yield s

def session_manager_for_class(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with session_maker() as session:
            try:
                result = await func(self, session, *args, **kwargs)
                return result
            except Exception as e:
                await session.rollback()
                raise e
    return wrapper

def session_manager(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_maker() as session:
            try:
                result = await func(session, *args, **kwargs)
                return result
            except Exception as e:
                await session.rollback()
                raise e
    return wrapper

