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
from app.api.handlers.product_handler import create_product, get_products_handler, get_product_by_id_handler, update_product_handler, delete_product_handler
from app.core.db import AsyncSessionDependency
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_route(product_data: ProductCreate, session: AsyncSessionDependency):
  return await create_product(product_data, session)

@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def get_products(session: AsyncSessionDependency):
  return await get_products_handler(session) 

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: int, session: AsyncSessionDependency):
  return await get_product_by_id_handler(product_id, session)

@router.patch("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def update_product(product_id: int, product: ProductUpdate, session: AsyncSessionDependency):
  return await update_product_handler(product_id, product, session)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: AsyncSessionDependency): 
  return await delete_product_handler(product_id, session)