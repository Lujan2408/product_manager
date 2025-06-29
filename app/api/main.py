# Main router for the API

from fastapi import APIRouter
from app.api.routers import product

api_router = APIRouter()

api_router.include_router(product.router, prefix="/products", tags=["Products"])

@api_router.get("/")
async def root():
  return {"message": "Hello from api/main.py"}
