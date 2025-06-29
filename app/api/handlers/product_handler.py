# ✅ RESPONSABILITIES OF HANDLER : 
# 1. Validate the data
# 2. Handle data of HTTP response
# 3. Convert data between HTTP and services
# 4. Handle errors HTTP 
# 5. MUST NOT contain business logic

from app.core.db import SessionDependency

async def create_product(product_data, session: SessionDependency):
  """Controlador para crear un producto"""
  
  result = product_data
  return {"message": "Product created successfully", "data": result, "status": "success"}