from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.session import Base

class UploadTask(Base):
    """Tasks for VA team to manually process products"""
    __tablename__ = "upload_tasks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)  # References Product.id
    status = Column(String, default="pending", index=True)  # pending, in_progress, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Index for VA team task management
    __table_args__ = (
        Index('ix_upload_tasks_status_created', 'status', 'created_at'),
    )