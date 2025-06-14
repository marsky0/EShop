from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase 
#from setttings.config import settings

class Base(DeclarativeBase):
    pass

#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
