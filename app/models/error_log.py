from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.db.session import Base

class ErrorLog(Base):
    """System error logging for debugging and monitoring"""
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, nullable=False, index=True)
    method = Column(String, nullable=False)
    error_type = Column(String, nullable=False, index=True)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    user_id = Column(String, nullable=True)
    request_data = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index('ix_error_logs_endpoint_created', 'endpoint', 'created_at'),
        Index('ix_error_logs_type_created', 'error_type', 'created_at'),
    )