from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True): 
  id: int = Field(default=None, primary_key=True)
  name: str = Field(index=True, min_length=3, max_length=255)
  price: float = Field(ge=0.0)
  available: bool = Field(default=True)