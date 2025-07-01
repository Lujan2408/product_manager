# ✅ RESPONSABILITIES OF SERVICE : 
# 1. Pure business logic (like create a product, get a product, update a product, delete a product)
# 2. Rules of business
# 3. Data business validation
# 4. Db operations
# 5. MUST NOT contain HTTP 

from app.core.db import AsyncSessionDependency
from app.models.products.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from sqlmodel import select

class ProductService:
    def __init__(self, session: AsyncSessionDependency):
        self.session = session

    async def create_product(self, product_data: ProductCreate):
        # Create the product
        product_data_dict = product_data.model_dump()
        product = Product(**product_data_dict)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)

        return product
    
    async def get_all_products(self):
        result = await self.session.execute(select(Product))
        return result.scalars().all()