# ✅ SCHEMAS RESPONSIBILITIES DTOs:
# 1. Data validation
# 2. Serialization/Deserialization of data
# 3. Auto generation of documentation
# 4. Data types transform 
# 5. MUST NOT interact with the database

from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Schema for creating a product (req)
class ProductCreate(BaseModel):
  name: str = Field(min_length=1, max_length=255, description="Product name")
  price: float = Field(gt=0, description="Product price")
  available: bool = Field(default=True, description="Product availability")

# Schema for the response of the product (res)
class ProductResponse(BaseModel): 
  id: int 
  name: str
  price: float
  available: bool
  created_at: datetime
  updated_at: datetime
  # The form_attributes allows the ORM (SQLModel) to convert the data from the database to the data of the response.
  class Config: 
    from_attributes = True

class ProductUpdate(BaseModel):
  name: Optional[str] = Field(default=None, min_length=1, max_length=255)
  price: Optional[float] = Field(default=None, gt=0)
  available: Optional[bool] = Field(default=None)

  @field_validator("name")
  def name_with_no_blank_spaces(cls, v):
    if v is not None and v.strip() == "":
      raise ValueError("Name cannot be blank")
    return v