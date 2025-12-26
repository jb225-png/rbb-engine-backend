from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.product import Product
from app.models.generation_job import GenerationJob
from app.models.upload_task import UploadTask
from app.core.enums import ProductStatus, JobStatus, UploadTaskStatus
from app.core.responses import success
from app.utils.logger import logger

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics with real data"""
    try:
        # Product counts by status
        product_stats = db.query(
            Product.status, func.count(Product.id)
        ).group_by(Product.status).all()
        
        products_by_status = {status.value: 0 for status in ProductStatus}
        for status, count in product_stats:
            products_by_status[status.value] = count
        
        # Generation job counts by status
        job_stats = db.query(
            GenerationJob.status, func.count(GenerationJob.id)
        ).group_by(GenerationJob.status).all()
        
        jobs_by_status = {status.value: 0 for status in JobStatus}
        for status, count in job_stats:
            jobs_by_status[status.value] = count
        
        # Upload task counts by status
        task_stats = db.query(
            UploadTask.status, func.count(UploadTask.id)
        ).group_by(UploadTask.status).all()
        
        tasks_by_status = {status.value: 0 for status in UploadTaskStatus}
        for status, count in task_stats:
            tasks_by_status[status.value] = count
        
        # Total counts
        total_products = sum(products_by_status.values())
        total_jobs = sum(jobs_by_status.values())
        total_tasks = sum(tasks_by_status.values())
        
        stats = {
            "total_products": total_products,
            "products_by_status": products_by_status,
            "total_generation_jobs": total_jobs,
            "jobs_by_status": jobs_by_status,
            "total_upload_tasks": total_tasks,
            "tasks_by_status": tasks_by_status
        }
        
        logger.info(f"Dashboard stats retrieved: {total_products} products, {total_jobs} jobs, {total_tasks} tasks")
        return success("Dashboard stats retrieved", stats)
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard stats: {e}")
        return success("Dashboard stats retrieved", {
            "total_products": 0,
            "products_by_status": {status.value: 0 for status in ProductStatus},
            "total_generation_jobs": 0,
            "jobs_by_status": {status.value: 0 for status in JobStatus},
            "total_upload_tasks": 0,
            "tasks_by_status": {status.value: 0 for status in UploadTaskStatus}
        })

@router.get("/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get lightweight dashboard summary"""
    try:
        total_products = db.query(func.count(Product.id)).scalar() or 0
        active_jobs = db.query(func.count(GenerationJob.id)).filter(
            GenerationJob.status.in_([JobStatus.PENDING, JobStatus.RUNNING])
        ).scalar() or 0
        pending_tasks = db.query(func.count(UploadTask.id)).filter(
            UploadTask.status == UploadTaskStatus.PENDING
        ).scalar() or 0
        
        summary = {
            "total_products": total_products,
            "active_jobs": active_jobs,
            "pending_tasks": pending_tasks
        }
        
        logger.info(f"Dashboard summary: {total_products} products, {active_jobs} active jobs, {pending_tasks} pending tasks")
        return success("Dashboard summary retrieved", summary)
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard summary: {e}")
        return success("Dashboard summary retrieved", {
            "total_products": 0,
            "active_jobs": 0,
            "pending_tasks": 0
        })