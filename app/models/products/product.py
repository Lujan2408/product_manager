# ✅ MODELS RESPONSIBILITIES:
# 1. Define the database schema
# 2. Define the relationships between tables
# 3. CRUD with the database

from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True): 
  id: int = Field(default=None, primary_key=True)
  name: str = Field(index=True, min_length=3, max_length=255)
  price: float = Field(ge=0.0)
  available: bool = Field(default=True)