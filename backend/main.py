from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from core.config import get_settings
from core.database import db
from core.exceptions import custom_exception_handler
from users.api import router as users_router
from vehicles.api import router as vehicles_router
from services.api import router as services_router
from history.api import router as history_router
from pricing.api import router as pricing_router
from emergency.api import router as emergency_router
from admin.api import router as admin_router

# Get settings
settings = get_settings()

# Define the base directory
BASE_DIR = settings.BASE_DIR

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI version of the MashinMan project",
    version=settings.PROJECT_VERSION
)

# Add custom exception handler
app.add_exception_handler(Exception, custom_exception_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=settings.STATIC_ROOT), name="static")
app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")

# Include routers
app.include_router(users_router)
app.include_router(vehicles_router)
app.include_router(services_router)
app.include_router(history_router)
app.include_router(pricing_router)
app.include_router(emergency_router)
app.include_router(admin_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to MashinMan API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)