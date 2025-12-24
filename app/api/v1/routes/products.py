from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.repositories.products import ProductRepository
from app.schemas.product import ProductRead, ProductCreate
from app.core.enums import Locale, CurriculumBoard, ProductType, ProductStatus
from app.core.responses import success
from app.utils.pagination import PaginationParams, paginate_query
from app.utils.logger import logger

router = APIRouter()

@router.post("/")
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create new product"""
    try:
        repo = ProductRepository(db)
        db_product = repo.create(product)
        logger.info(f"Created product: {db_product.product_type} for standard {db_product.standard_id} (ID: {db_product.id})")
        return success("Product created successfully", ProductRead.model_validate(db_product))
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_products(
    status: Optional[ProductStatus] = Query(None),
    product_type: Optional[ProductType] = Query(None),
    generation_job_id: Optional[int] = Query(None),
    standard_id: Optional[int] = Query(None),
    curriculum_board: Optional[CurriculumBoard] = Query(None),
    grade_level: Optional[int] = Query(None),
    locale: Optional[Locale] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all products with filtering and pagination"""
    try:
        repo = ProductRepository(db)
        query = repo.get_all(status, product_type, generation_job_id, standard_id, curriculum_board, grade_level, locale)
        
        pagination_params = PaginationParams(limit=limit, offset=offset)
        paginated_result = paginate_query(query, pagination_params)
        
        products_data = [ProductRead.model_validate(product) for product in paginated_result.items]
        
        return success("Products retrieved successfully", {
            "products": products_data,
            "pagination": {
                "total": paginated_result.total,
                "limit": paginated_result.limit,
                "offset": paginated_result.offset,
                "has_next": paginated_result.has_next
            }
        })
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get specific product details"""
    try:
        repo = ProductRepository(db)
        product = repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
@router.patch("/{product_id}/status")
async def update_product_status(
    product_id: int,
    status: ProductStatus,
    db: Session = Depends(get_db)
):
    """Update product status with validation and job status tracking"""
    try:
        repo = ProductRepository(db)
        product = repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Validate status transitions
        valid_transitions = {
            ProductStatus.DRAFT: [ProductStatus.GENERATED, ProductStatus.FAILED],
            ProductStatus.GENERATED: [ProductStatus.FAILED],
            ProductStatus.FAILED: [ProductStatus.DRAFT]
        }
        
        if status not in valid_transitions.get(product.status, []):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid status transition from {product.status.value} to {status.value}"
            )
        
        # Update product status
        updated_product = repo.update_status(product_id, status)
        
        # Update associated generation job status
        if updated_product.generation_job_id:
            from app.services.job_status import update_job_status
            update_job_status(db, updated_product.generation_job_id)
        
        logger.info(f"Updated product {product_id} status from {product.status} to {status}")
        
        return success("Product status updated", {
            "id": product_id, 
            "status": status.value,
            "previous_status": product.status.value,
            "product": ProductRead.model_validate(updated_product)
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product {product_id} status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")