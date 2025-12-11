from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.session import Base

class Standard(Base):
    """Educational standards that define content generation requirements"""
    __tablename__ = "standards"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)  # e.g., "CCSS.MATH.1.OA.1"
    description = Column(String, nullable=True)  # Human-readable description
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Index for common queries
    __table_args__ = (
        Index('ix_standards_code', 'code'),
    )