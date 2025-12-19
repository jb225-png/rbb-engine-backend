from sqlalchemy import Column, Integer, String, DateTime, Index, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.enums import Locale, CurriculumBoard, JobStatus, JobType

class GenerationJob(Base):
    """Jobs that generate products from standards (manual or n8n triggered)"""
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, nullable=False, index=True)  # References Standard.id
    locale = Column(Enum(Locale), nullable=False, default=Locale.IN, index=True)
    curriculum_board = Column(Enum(CurriculumBoard), nullable=False, default=CurriculumBoard.CBSE, index=True)
    grade_level = Column(Integer, nullable=False, index=True)
    job_type = Column(Enum(JobType), nullable=False, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, index=True)
    total_products = Column(Integer, default=0)  # Total products to generate
    completed_products = Column(Integer, default=0)  # Successfully completed
    failed_products = Column(Integer, default=0)  # Failed products
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('ix_generation_jobs_locale_curriculum', 'locale', 'curriculum_board'),
        Index('ix_generation_jobs_status_created', 'status', 'created_at'),
        Index('ix_generation_jobs_standard_type', 'standard_id', 'job_type'),
    )