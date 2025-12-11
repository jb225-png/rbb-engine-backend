from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.session import Base

class FileArtifact(Base):
    """Files associated with products (raw.json, final.json, metadata.json, zip bundles)"""
    __tablename__ = "file_artifacts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)  # References Product.id
    file_type = Column(String, nullable=False, index=True)  # raw_json, final_json, metadata_json, zip_bundle
    file_path = Column(String, nullable=False)  # Relative path to file in storage
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Index for file management and cleanup
    __table_args__ = (
        Index('ix_file_artifacts_product_type', 'product_id', 'file_type'),
    )