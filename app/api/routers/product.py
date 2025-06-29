# ✅ RESPONSABILITIES OF ROUTER : 
# 1. Define the HTTP routes for the product router
# 2. Define the HTTP methods for the product router
# 3. Define the HTTP status codes for the product router
# 4. Define the HTTP headers for the product router
# 5. Define the HTTP body for the product router
# 6. Define the HTTP query parameters for the product router

from fastapi import APIRouter
from app.api.handlers.product_handler import create_product
from app.core.db import SessionDependency
from app.schemas.product import ProductCreate

router = APIRouter()

# Only define routes (endpoints) 
# Here is where we define the routes for the product router

# @router.post("/")
# async def create_product_route(product_data: ProductCreate, session: SessionDependency):
#   return create_product(product_data, session)

@router.get("/")
async def get_products():
  return {"message": "Getting products ..." , "from": "routers/product.py"}