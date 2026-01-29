from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.schemas.generate import GenerateProductRequest, GenerateProductResponse
from app.models.generation_job import GenerationJob
from app.models.product import Product
from app.models.standard import Standard
from app.core.enums import JobType, JobStatus, ProductStatus
from app.utils.logger import logger
from app.utils.storage import storage_manager
from app.utils.pdf_stub import generate_stub_pdf
from app.utils.thumbnail_stub import generate_stub_thumbnail
from app.utils.validation import validate_positive_integer, validate_grade_level
from app.services.job_status import update_job_progress

# AI Agents
from app.ai.agents.generator import generator_agent
from app.ai.agents.qc import qc_agent
from app.ai.agents.metadata import metadata_agent

router = APIRouter()

@router.post("/generate-product", response_model=GenerateProductResponse)
async def generate_product(
    request: GenerateProductRequest,
    db: Session = Depends(get_db)
):
    """Generate product endpoint with full AI agent orchestration"""
    
    # Validate input fields using standardized validators
    validate_positive_integer(request.standard_id, "standard_id")
    validate_grade_level(request.grade_level)
    
    try:
        # Get standard information for AI generation
        standard = db.query(Standard).filter(Standard.id == request.standard_id).first()
        if not standard:
            raise HTTPException(status_code=404, detail="Standard not found")
        
        # Use transaction for atomic creation
        try:
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
            db.flush()  # Get product ID
            
            # Create storage structure and stub files
            try:
                storage_manager.create_stub_files(product.id)
                generate_stub_pdf(product.id, request.product_type.value)
                generate_stub_thumbnail(product.id, request.product_type.value)
            except Exception as storage_error:
                logger.warning(f"Storage setup failed for product {product.id}: {storage_error}")
                # Continue - storage issues shouldn't fail the entire operation
            
            db.commit()
        except Exception as db_error:
            db.rollback()
            raise db_error
        
        # AI Agent Orchestration (Sequential)
        try:
            logger.info(f"Starting AI generation for product {product.id}")
            
            # Step 1: Generate Content
            content = await generator_agent.generate_content(
                product_id=product.id,
                product_type=request.product_type.value,
                standard=standard.description or standard.code,
                grade_level=request.grade_level,
                curriculum=request.curriculum_board.value
            )
            
            # Step 2: Quality Control
            qc_result = await qc_agent.evaluate_content(
                product_id=product.id,
                product_type=request.product_type.value,
                content=content,
                standard=standard.description or standard.code,
                grade_level=request.grade_level
            )
            
            # Step 3: Generate Metadata
            metadata = await metadata_agent.generate_metadata(
                product_id=product.id,
                product_type=request.product_type.value,
                content=content,
                standard=standard.description or standard.code,
                grade_level=request.grade_level,
                curriculum=request.curriculum_board.value
            )
            
            # Update product status based on QC result
            if qc_result['verdict'] == 'PASS':
                product.status = ProductStatus.GENERATED
                logger.info(f"Product {product.id} generated successfully (QC: {qc_result['score']}%)")
            else:
                product.status = ProductStatus.FAILED
                logger.warning(f"Product {product.id} failed QC: {qc_result['verdict']} (score: {qc_result['score']}%)")
            
            db.commit()
            
            # Update job progress
            update_job_progress(db, job.id, product.id, product.status)
            
        except Exception as ai_error:
            logger.error(f"AI generation failed for product {product.id}: {ai_error}")
            # Mark product as failed
            product.status = ProductStatus.FAILED
            db.commit()
            update_job_progress(db, job.id, product.id, ProductStatus.FAILED)
            
        logger.info(
            f"Generated job {job.id} with product {product.id}: "
            f"{request.product_type.value} for standard {request.standard_id} "
            f"(Grade {request.grade_level}, {request.curriculum_board.value}) - Status: {product.status.value}"
        )
        
        return GenerateProductResponse(
            job_id=job.id,
            product_ids=[product.id],
            message=f"Product generation completed for {request.product_type.value} - Status: {product.status.value}"
        )
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in generate_product: {e}")
        raise HTTPException(status_code=500, detail="Failed to create generation job")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in generate_product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")