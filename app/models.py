'''

This code defines Pydantic models for equipment and user schemas, along with corresponding SQLAlchemy models.

It includes configurations for JSON schema examples and establishes a function to get an asynchronous database session.

The models represent equipment details, user details, and login credentials.

'''

from pydantic import BaseModel, Field, EmailStr, validator
from sqlalchemy import Column, Integer, String
from typing import Optional
import uuid
from app.database import Base, SessionLocal, engine


# sqlalchemy database schema for storing sports equipment details
class EquipmentSchemaDB(Base):
    __tablename__ = "equipments"
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=False)
    quantity =  Column(Integer, nullable=False)
    owner_email =  Column(String, nullable=False)
    
 
# Pydantic model for taking equipment details from user 
class EquipmentSchema(BaseModel):
    item: str = Field(nullable=False)
    quantity: int = Field(nullable=False)
    class Config:
        json_schema_extra = {
            "equipment_demo": {
                "item": "Cricket bat",
                "quantity": 223,
            }
        }


# Pydantic model for taking user details
class UserSchema(BaseModel):
    name: str = Field(default=None, nullable=False)
    email: EmailStr = Field(default=None, unique=True, nullable=False)
    password: str = Field(default=None, nullable=False)
    class Config:
        json_schema_extra = {
            "user_demo": {
                "name": "Dave Bautisita",
                "email": "daveb@wwe.com",
                "password": "wwe123"
            }
        }


# sqlalchemy database schema for storing user details
class UserSchemaDB(Base):
    __tablename__ = "users_registered"
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, primary_key=True)
    password = Column(String, nullable=False)


# Pydantic model for taking user login credentials from user
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    class Config:
        json_schema_extra = {
            "user_demo": {
                "email": "daveb@wwe.com",
                "password": "wwe123"
            }
        }


# method to create and close database connection
async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()