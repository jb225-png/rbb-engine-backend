from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.generation_job import GenerationJobCreate, GenerationJobRead
from app.core.responses import success

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    # TODO: implement actual stats queries
    return success("Dashboard stats retrieved", {
        "total_products": 0,
        "active_jobs": 0,
        "pending_tasks": 0
    })

@router.post("/quick-generate")
async def quick_generate(job: GenerationJobCreate, db: Session = Depends(get_db)):
    """Quick generation trigger from dashboard"""
    # TODO: implement job creation and trigger
    return success("Generation job created", {
        "job_id": 1,
        "status": "pending"
    })