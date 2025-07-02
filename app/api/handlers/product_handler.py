# ✅ RESPONSABILITIES OF HANDLER : 
# 1. Validate the data
# 2. Handle data of HTTP response
# 3. Convert data between HTTP and services
# 4. Handle errors HTTP 
# 5. MUST NOT contain business logic

from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from app.core.db import AsyncSessionDependency
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.errors.product_errors import ProductNotFoundError, DuplicateProductNameError, NoFieldsToUpdateError

async def create_product(product_data: ProductCreate, session: AsyncSessionDependency):
  try: 
    # Create the service
    service = ProductService(session)
    # Call business logic 
    product = await service.create_product(product_data)
    
    # Format HTTP response 
    return {
      "message": "Product created successfully",
      "data": ProductResponse.model_validate(product).model_dump(),
      "status": "success"
    }

  except DuplicateProductNameError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error ocurred")
  
async def get_products_handler(session: AsyncSessionDependency):
  try:
    service = ProductService(session)
    products = await service.get_all_products()
    return products
  
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error ocurred")
  
async def get_product_by_id_handler(product_id: int, session: AsyncSessionDependency):
  try: 
    service = ProductService(session)
    product = await service.get_product_by_id(product_id)

    return product
  
  except ProductNotFoundError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error ocurred")
    
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
  
async def delete_product_handler(product_id: int, session: AsyncSessionDependency):
  try: 
    service = ProductService(session)
    await service.delete_product(product_id)
  
    return JSONResponse(
      content={
        "message": f"Product with ID: {product_id} deleted successfully",
        "status": "success"
      },
      status_code=status.HTTP_200_OK
    )
  
  except ProductNotFoundError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error ocurred")
  
  