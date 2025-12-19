from sqlalchemy import Column, Integer, String, DateTime, Index, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.enums import UploadTaskStatus

class UploadTask(Base):
    """Tasks for VA team to manually process products"""
    __tablename__ = "upload_tasks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)  # References Product.id
    status = Column(Enum(UploadTaskStatus), default=UploadTaskStatus.PENDING, index=True)
    assigned_to = Column(String, nullable=True)  # VA team member
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Index for VA team task management
    __table_args__ = (
        Index('ix_upload_tasks_status_created', 'status', 'created_at'),
        Index('ix_upload_tasks_assigned', 'assigned_to'),
    )