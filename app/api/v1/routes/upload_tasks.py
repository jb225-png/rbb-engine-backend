from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.schemas.upload_task import UploadTaskRead, UploadTaskCreate, UploadTaskUpdate
from app.models.upload_task import UploadTask
from app.core.enums import UploadTaskStatus
from app.core.responses import success
from app.utils.logger import logger

router = APIRouter()

@router.post("/", response_model=UploadTaskRead)
async def create_upload_task(
    task: UploadTaskCreate,
    db: Session = Depends(get_db)
):
    """Create new upload task"""
    db_task = UploadTask(
        product_id=task.product_id,
        status=task.status or UploadTaskStatus.PENDING,
        assigned_to=task.assigned_to
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    logger.info(f"Created upload task {db_task.id} for product {task.product_id}")
    return db_task

@router.get("/")
async def list_upload_tasks(
    status: Optional[UploadTaskStatus] = Query(None),
    assigned_to: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List upload tasks with filtering and pagination"""
    query = db.query(UploadTask)
    
    if status:
        query = query.filter(UploadTask.status == status)
    if assigned_to:
        query = query.filter(UploadTask.assigned_to == assigned_to)
    
    total = query.count()
    tasks = query.offset(offset).limit(limit).all()
    
    return success("Upload tasks retrieved", {
        "tasks": [UploadTaskRead.model_validate(task) for task in tasks],
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_next": offset + limit < total
        }
    })

@router.get("/{task_id}", response_model=UploadTaskRead)
async def get_upload_task(task_id: int, db: Session = Depends(get_db)):
    """Get specific upload task"""
    task = db.query(UploadTask).filter(UploadTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Upload task not found")
    return task

@router.patch("/{task_id}")
async def update_upload_task(
    task_id: int,
    task_update: UploadTaskUpdate,
    db: Session = Depends(get_db)
):
    """Update upload task"""
    task = db.query(UploadTask).filter(UploadTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Upload task not found")
    
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.assigned_to is not None:
        task.assigned_to = task_update.assigned_to
    
    db.commit()
    db.refresh(task)
    
    logger.info(f"Updated upload task {task_id}")
    return success("Upload task updated", UploadTaskRead.model_validate(task))