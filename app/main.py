# Main file for the API

from fastapi import FastAPI
from app.api.main import router
from app.core.db import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/products")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)