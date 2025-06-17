from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase 
from functools import wraps

#from setttings.config import settings

class Base(DeclarativeBase):
    pass

#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
session_maker = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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


'''
def get_session():
    s = session()
    try:
        yield s
    finally:
        s.close()
'''
