# ✅ SCHEMAS RESPONSIBILITIES DTOs:
# 1. Data validation
# 2. Serialization/Deserialization of data
# 3. Auto generation of documentation
# 4. Data types transform 
# 5. MUST NOT interact with the database

from pydantic import BaseModel

class ProductCreate(BaseModel):
  name: str
  price: float
  available: bool = True