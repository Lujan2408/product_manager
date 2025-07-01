# ✅ RESPONSABILITIES OF HANDLER : 
# 1. Validate the data
# 2. Handle data of HTTP response
# 3. Convert data between HTTP and services
# 4. Handle errors HTTP 
# 5. MUST NOT contain business logic

from fastapi import HTTPException, status
from sqlmodel import select
from app.core.db import AsyncSessionDependency
from app.models.products.product import Product
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.errors.product_errors import ProductNotFoundError, DuplicateProductNameError, NoFieldsToUpdateError

async def create_product(product_data: ProductCreate, session: AsyncSessionDependency):
  try: 
    # Create the service
    service = ProductService(session)

    # Check if a product already exists with the same name
    result = await session.execute(select(Product).where(Product.name == product_data.name))
    existing_product = result.first()

    if existing_product:
        raise ValueError(f"Product with name {product_data.name} already exists")

    # Call business logic 
    product = await service.create_product(product_data)
    # Format HTTP response 
    return {
      "message": "Product created successfully",
      "data": ProductResponse.model_validate(product).model_dump(),
      "status": "success"
    }

  # Handle business errors 
  except ValueError as e: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  # Handle unexpected errors 
  except Exception as e: 
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
async def get_products_handler(session: AsyncSessionDependency):
  try:
    service = ProductService(session)
    products = await service.get_all_products()
    return products
  
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
async def get_product_by_id_handler(product_id: int, session: AsyncSessionDependency):
  try: 
    service = ProductService(session)
    product = await service.get_product_by_id(product_id)

    if not product: 
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or does not exist")
    
    return product
  
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def update_product_handler(product_id: int, product_data: ProductUpdate, session: AsyncSessionDependency):
  try: 
    service = ProductService(session)
    product = await service.update_product(product_id, product_data)

    return ProductResponse.model_validate(product).model_dump(exclude_unset=True)
  
  except ProductNotFoundError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
  except DuplicateProductNameError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except NoFieldsToUpdateError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error ocurred")