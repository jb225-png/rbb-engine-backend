from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    """Enhanced health check endpoint with service info"""
    return {
        "status": "ok",
        "service": "rbb-backend",
        "env": settings.environment
    }
