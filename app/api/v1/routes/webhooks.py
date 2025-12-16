from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from app.db.session import get_db
from app.schemas.workflow import GenerationRequestPayload
from app.schemas.generation_job import GenerationJobCreate
from app.utils.logger import logger
from app.core.responses import success

router = APIRouter()

@router.post("/generation-request")
async def webhook_generation_request(
    payload: GenerationRequestPayload,
    db: Session = Depends(get_db)
):
    """Webhook endpoint for n8n generation requests"""
    request_id = str(uuid.uuid4())
    
    # Log workflow request
    logger.info(f"Webhook request received - ID: {request_id}, Source: {payload.source}, Standard: {payload.standard_code}")
    
    # Create generation job using existing logic
    job_data = GenerationJobCreate(
        standard_id=1,  # TODO: lookup standard by code
        job_type="workflow_bundle"
    )
    
    # TODO: Call existing generation job creation service
    # For now, return success response
    
    logger.info(f"Generation job created for webhook request {request_id}")
    
    return success("Generation request received", {
        "request_id": request_id,
        "status": "accepted"
    })