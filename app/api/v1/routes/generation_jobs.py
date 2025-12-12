from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.generation_job import GenerationJob
from app.schemas.generation_job import GenerationJobRead, GenerationJobCreate
from app.core.enums import JobStatus, JobType

router = APIRouter()

@router.post("/", response_model=GenerationJobRead)
async def create_generation_job(job: GenerationJobCreate, db: Session = Depends(get_db)):
    """Create new generation job"""
    job_data = job.model_dump()
    job_data['status'] = JobStatus.PENDING
    db_job = GenerationJob(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[GenerationJobRead])
async def list_generation_jobs(
    status: Optional[JobStatus] = Query(None),
    job_type: Optional[JobType] = Query(None),
    db: Session = Depends(get_db)
):
    """List all generation jobs with optional filtering"""
    query = db.query(GenerationJob)
    if status:
        query = query.filter(GenerationJob.status == status)
    if job_type:
        query = query.filter(GenerationJob.job_type == job_type)
    return query.all()

@router.get("/{job_id}", response_model=GenerationJobRead)
async def get_generation_job(job_id: int, db: Session = Depends(get_db)):
    """Get specific job details and progress"""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Generation job not found")
    return job