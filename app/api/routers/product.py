# ✅ RESPONSABILITIES OF ROUTER : 
# 1. Define the HTTP routes for the product router
# 2. Define the HTTP methods for the product router
# 3. Define the HTTP status codes for the product router
# 4. Define the HTTP headers for the product router
# 5. Define the HTTP body for the product router
# 6. Define the HTTP query parameters for the product router
# 7. Only define routes (endpoints) 
# 8. Here is where we define the routes for the product router

from fastapi import APIRouter, status
from app.api.handlers.product_handler import create_product
from app.core.db import SessionDependency
from app.schemas.product import ProductCreate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_route(product_data: ProductCreate, session: SessionDependency):
  return await create_product(product_data, session)