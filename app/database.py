'''
This code sets up SQLAlchemy for asynchronous operations with an SQLite database.
It defines the database URL, creates an asynchronous database engine, and establishes an asynchronous session for database interactions.

The `Base` variable represents the declarative base for defining models.

'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./equipments.db"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()