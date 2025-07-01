# ✅ RESPONSABILITIES OF SERVICE : 
# 1. Pure business logic (like create a product, get a product, update a product, delete a product)
# 2. Rules of business
# 3. Data business validation
# 4. Db operations
# 5. MUST NOT contain HTTP 

from app.core.db import AsyncSessionDependency
from app.models.products.product import Product
from app.schemas.product import ProductCreate
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

class ProductService:
    def __init__(self, session: AsyncSessionDependency):
        self.session = session

    async def create_product(self, product_data: ProductCreate):
        # Data validation
        if product_data.price <= 0: 
            raise ValueError("Price must be greater than 0")
        
        # Check if a product already exists with the same name
        result = await self.session.execute(select(Product).where(Product.name == product_data.name))
        existing_product = result.first()

        if existing_product:
            raise ValueError(f"Product with name {product_data.name} already exists")
        
        # Create the product
        product_data_dict = product_data.model_dump()
        product = Product(**product_data_dict)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)

        return product