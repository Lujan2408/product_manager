# ✅ RESPONSABILITIES OF HANDLER : 
# 1. Validate the data
# 2. Handle data of HTTP response
# 3. Convert data between HTTP and services
# 4. Handle errors HTTP 
# 5. MUST NOT contain business logic

from fastapi import HTTPException, status
from app.core.db import SessionDependency
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductResponse

async def create_product(product_data: ProductCreate, session: SessionDependency):
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

  except Exception as e:
    # Handle business errors 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except Exception as e:
    # Handle unexpected errors 
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))