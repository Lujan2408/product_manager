# ✅ MODELS RESPONSIBILITIES:
# 1. Define the database schema
# 2. Define the relationships between tables
# 3. CRUD with the database

from datetime import date
from sqlmodel import Field, SQLModel, Column, Float
from sqlalchemy import DateTime as SQLAlchemyDateTime

class Product(SQLModel, table=True): 
  id: int = Field(default=None, primary_key=True)
  name: str = Field(index=True, min_length=3, max_length=255)
  price: float = Field(ge=0, sa_column=Column(Float))
  available: bool = Field(default=True)
  created_at: date = Field(default_factory=date.today, sa_column=Column(SQLAlchemyDateTime, default=date.today))
  updated_at: date = Field(default_factory=date.today, sa_column=Column(SQLAlchemyDateTime, default=date.today, onupdate=date.today))