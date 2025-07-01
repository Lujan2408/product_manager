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
from app.api.handlers.product_handler import get_products as get_products_handler
from app.core.db import AsyncSessionDependency
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_route(product_data: ProductCreate, session: AsyncSessionDependency):
  return await create_product(product_data, session)

@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def get_products(session: AsyncSessionDependency):
  return await get_products_handler(session) 
