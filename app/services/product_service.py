# ✅ RESPONSABILITIES OF SERVICE : 
# 1. Pure business logic (like create a product, get a product, update a product, delete a product)
# 2. Rules of business
# 3. Data business validation
# 4. Db operations
# 5. MUST NOT contain HTTP 

from app.core.db import SessionDependency
from app.schemas.product import ProductCreate

class ProductService:
    def __init__(self, session: SessionDependency):
        self.session = session

    async def create_product(self, product_data: ProductCreate):
        """Business logic for creating a product"""
        # Business rules, validations, db operations, etc.
        return {"message": "Creating product from services/product_service.py", "data": product_data}