from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.session import Base

class GenerationJob(Base):
    """Jobs that generate products from standards (manual or n8n triggered)"""
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, nullable=False, index=True)  # References Standard.id
    job_type = Column(String, nullable=False, index=True)  # single_product, full_bundle
    status = Column(String, default="pending", index=True)  # pending, running, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes for job tracking and filtering
    __table_args__ = (
        Index('ix_generation_jobs_status_created', 'status', 'created_at'),
        Index('ix_generation_jobs_standard_type', 'standard_id', 'job_type'),
    )