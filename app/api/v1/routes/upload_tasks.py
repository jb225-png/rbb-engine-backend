from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.upload_task import UploadTaskRead, UploadTaskUpdate

router = APIRouter()

@router.get("/", response_model=List[UploadTaskRead])
async def list_upload_tasks(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List upload tasks for VA team"""
    # TODO: implement DB query with status filter
    return []

@router.put("/{task_id}", response_model=UploadTaskRead)
async def update_upload_task(
    task_id: int, 
    task_update: UploadTaskUpdate, 
    db: Session = Depends(get_db)
):
    """Update upload task status"""
    # TODO: implement DB update and 404 handling
    return UploadTaskRead(
        id=task_id,
        product_id=1,
        status=task_update.status,
        created_at="2024-01-01T00:00:00Z"
    )