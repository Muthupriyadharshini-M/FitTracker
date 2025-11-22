from fastapi import FastAPI
from api.v1 import user_routes, meal_log_routes, exercise_log_routes

app = FastAPI(
    title="FitTracker API",
    description="Enterprise fitness tracking application",
    version="1.0.0"
)

# Include API routers
app.include_router(user_routes.router, prefix="/api/v1", tags=["users"])
app.include_router(meal_log_routes.router, prefix="/api/v1", tags=["meal_logs"])
app.include_router(exercise_log_routes.router, prefix="/api/v1", tags=["exercise_logs"])

@app.get("/")
async def root():
    return {"message": "Welcome to FitTracker API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
