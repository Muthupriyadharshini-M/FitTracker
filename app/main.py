from fastapi import FastAPI
from api.v1 import user_routes

app = FastAPI(
    title="FitTracker API",
    description="Enterprise fitness tracking application",
    version="1.0.0"
)

# Include API routers
app.include_router(user_routes.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to FitTracker API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
