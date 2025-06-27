from fastapi import FastAPI

app = FastAPI(
    title="Product Manager API",
    description="A FastAPI backend for product management",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Product Manager API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "product-manager"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)