# Main router for the API

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to Product Manager API", "status": "running"}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "product-manager"}