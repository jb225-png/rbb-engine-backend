from fastapi import APIRouter
from app.core.responses import success

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return success("Service is healthy", {"status": "ok", "version": "1.0.0"})
