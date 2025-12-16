from sqlalchemy import Column, Integer, DateTime, Index, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.enums import Locale, CurriculumBoard, ProductType, ProductStatus

class Product(Base):
    """Generated educational content items (worksheets, passages, quizzes, etc.)"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, nullable=False, index=True)  # References Standard.id
    generation_job_id = Column(Integer, nullable=True, index=True)  # References GenerationJob.id
    product_type = Column(Enum(ProductType), nullable=False, index=True)
    status = Column(Enum(ProductStatus), default=ProductStatus.DRAFT, index=True)
    locale = Column(Enum(Locale), nullable=False, default=Locale.IN, index=True)
    curriculum_board = Column(Enum(CurriculumBoard), nullable=False, default=CurriculumBoard.CBSE, index=True)
    grade_level = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('ix_products_generation_job_id', 'generation_job_id'),
        Index('ix_products_status_type', 'status', 'product_type'),
        Index('ix_products_standard_status', 'standard_id', 'status'),
    )
