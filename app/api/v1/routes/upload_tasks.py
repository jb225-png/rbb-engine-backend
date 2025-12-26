from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from app.db.session import get_db
from app.schemas.upload_task import UploadTaskRead, UploadTaskCreate, UploadTaskUpdate
from app.models.upload_task import UploadTask
from app.core.enums import UploadTaskStatus
from app.core.responses import success, error
from app.utils.logger import logger

router = APIRouter()

@router.post("/", response_model=UploadTaskRead)
async def create_upload_task(
    task: UploadTaskCreate,
    db: Session = Depends(get_db)
):
    """Create new upload task with product validation"""
    try:
        # Validate product exists
        from app.models.product import Product
        product = db.query(Product).filter(Product.id == task.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {task.product_id} not found")
        
        db_task = UploadTask(
            product_id=task.product_id,
            status=task.status or UploadTaskStatus.PENDING,
            assigned_to=task.assigned_to
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        logger.info(f"Created upload task {db_task.id} for product {task.product_id} (type: {product.product_type.value})")
        return db_task
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating upload task: {e}")
        raise HTTPException(status_code=500, detail="Failed to create upload task")
    except Exception as e:
        logger.error(f"Error creating upload task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/")
async def list_upload_tasks(
    status: Optional[UploadTaskStatus] = Query(None),
    assigned_to: Optional[str] = Query(None),
    product_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List upload tasks with enhanced filtering and product context"""
    try:
        from app.models.product import Product
        
        # Join with Product for better context
        query = db.query(UploadTask).join(Product, UploadTask.product_id == Product.id)
        
        if status:
            query = query.filter(UploadTask.status == status)
        if assigned_to:
            query = query.filter(UploadTask.assigned_to == assigned_to)
        if product_id:
            query = query.filter(UploadTask.product_id == product_id)
        
        total = query.count()
        tasks = query.order_by(UploadTask.created_at.desc()).offset(offset).limit(limit).all()
        
        # Log filtering info
        filters_applied = []
        if status: filters_applied.append(f"status={status.value}")
        if assigned_to: filters_applied.append(f"assigned_to={assigned_to}")
        if product_id: filters_applied.append(f"product_id={product_id}")
        
        filter_str = ", ".join(filters_applied) if filters_applied else "no filters"
        logger.info(f"Listed {len(tasks)} upload tasks (total: {total}) with {filter_str}")
        
        return success("Upload tasks retrieved", {
            "tasks": [UploadTaskRead.model_validate(task) for task in tasks],
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_next": offset + limit < total
            }
        })
    except Exception as e:
        logger.error(f"Error listing upload tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{task_id}", response_model=UploadTaskRead)
async def get_upload_task(task_id: int, db: Session = Depends(get_db)):
    """Get specific upload task with proper error handling"""
    try:
        task = db.query(UploadTask).filter(UploadTask.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Upload task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting upload task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/{task_id}")
async def update_upload_task(
    task_id: int,
    task_update: UploadTaskUpdate,
    db: Session = Depends(get_db)
):
    """Update upload task with status transition validation"""
    try:
        task = db.query(UploadTask).filter(UploadTask.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Upload task not found")
        
        # Validate status transitions if status is being updated
        if task_update.status is not None:
            valid_transitions = {
                UploadTaskStatus.PENDING: [UploadTaskStatus.IN_PROGRESS],
                UploadTaskStatus.IN_PROGRESS: [UploadTaskStatus.COMPLETED, UploadTaskStatus.PENDING],
                UploadTaskStatus.COMPLETED: []  # Terminal state
            }
            
            if task_update.status not in valid_transitions.get(task.status, []):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid status transition from {task.status.value} to {task_update.status.value}"
                )
            
            task.status = task_update.status
        
        if task_update.assigned_to is not None:
            task.assigned_to = task_update.assigned_to
        
        db.commit()
        db.refresh(task)
        
        logger.info(f"Updated upload task {task_id}: status={task.status}, assigned_to={task.assigned_to}")
        return success("Upload task updated", UploadTaskRead.model_validate(task))
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating upload task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update upload task")
    except Exception as e:
        logger.error(f"Error updating upload task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")