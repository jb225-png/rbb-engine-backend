from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.session import Base

class Product(Base):
    """Generated educational content items (worksheets, passages, quizzes, etc.)"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, nullable=False, index=True)  # References Standard.id
    type = Column(String, nullable=False, index=True)  # worksheet, passage, quiz, etc.
    status = Column(String, default="draft", index=True)  # draft, generated, reviewed, published
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes for common filtering
    __table_args__ = (
        Index('ix_products_standard_status', 'standard_id', 'status'),
        Index('ix_products_type_status', 'type', 'status'),
    )
