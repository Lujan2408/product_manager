# ✅ RESPONSABILITIES OF SERVICE : 
# 1. Pure business logic (like create a product, get a product, update a product, delete a product)
# 2. Rules of business
# 3. Data business validation
# 4. Db operations
# 5. MUST NOT contain HTTP 

from app.core.db import AsyncSessionDependency
from app.models.products.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.errors.product_errors import ProductNotFoundError, DuplicateProductNameError, NoFieldsToUpdateError
from sqlmodel import select

class ProductService:
    def __init__(self, session: AsyncSessionDependency):
        self.session = session

    async def create_product(self, product_data: ProductCreate):

        # Check if a product already exists with the same name
        existing_product = await self.session.execute(select(Product).where(Product.name == product_data.name))
        if existing_product.first():
            raise DuplicateProductNameError(f"Product with name {product_data.name} already exists")

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
    
    async def get_product_by_id(self, product_id: int):
        product_db = await self.session.get(Product, product_id)

        if not product_db: 
            raise ProductNotFoundError("Product not found or does not exist")

        return product_db
    
    async def update_product(self, product_id: int, product_data: ProductUpdate):
        product_db = await self.session.get(Product, product_id)

        # Check if the product exists
        if not product_db:
            raise ProductNotFoundError("Product not found or does not exist")
        
        # Check if at least one field is provided to update the product
        if not any([
            product_data.name is not None,
            product_data.price is not None,
            product_data.available is not None
        ]):
            raise NoFieldsToUpdateError("At least one field must be provided to update the product")
        
        # Check if already exists a product with the same name
        if product_data.name and product_data.name != product_db.name: 
            result = await self.session.execute(select(Product).where(Product.name == product_data.name))
            existing_product = result.scalar_one_or_none()
            if existing_product:
                raise DuplicateProductNameError(f"Product with name {product_data.name} already exists")

        product_db.sqlmodel_update(product_data)
        self.session.add(product_db)
        await self.session.commit()
        await self.session.refresh(product_db)

        return product_db