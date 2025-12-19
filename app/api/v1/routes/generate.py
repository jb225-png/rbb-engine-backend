from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.generate import GenerateProductRequest, GenerateProductResponse
from app.models.generation_job import GenerationJob
from app.models.product import Product
from app.core.enums import JobType, JobStatus, ProductStatus
from app.utils.logger import logger

router = APIRouter()

@router.post("/generate-product", response_model=GenerateProductResponse)
async def generate_product(
    request: GenerateProductRequest,
    db: Session = Depends(get_db)
):
    """Generate product endpoint - creates job and product records"""
    
    # Create generation job
    job = GenerationJob(
        standard_id=request.standard_id,
        locale=request.locale,
        curriculum_board=request.curriculum_board,
        grade_level=request.grade_level,
        job_type=JobType.SINGLE_PRODUCT,
        status=JobStatus.PENDING,
        total_products=1,
        completed_products=0,
        failed_products=0
    )
    db.add(job)
    db.flush()  # Get job ID
    
    # Create product record
    product = Product(
        standard_id=request.standard_id,
        generation_job_id=job.id,
        product_type=request.product_type,
        status=ProductStatus.DRAFT,
        locale=request.locale,
        curriculum_board=request.curriculum_board,
        grade_level=request.grade_level
    )
    db.add(product)
    db.commit()
    
    logger.info(f"Generated product job {job.id} with product {product.id}")
    
    return GenerateProductResponse(
        job_id=job.id,
        product_ids=[product.id],
        message="Product generation job created successfully"
    )