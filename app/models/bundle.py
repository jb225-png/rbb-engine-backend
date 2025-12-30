from sqlalchemy import Column, Integer, String, DateTime, Index, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.enums import Locale, CurriculumBoard

class Bundle(Base):
    """Product bundles for grouped content delivery"""
    __tablename__ = "bundles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    locale = Column(Enum(Locale), nullable=False, default=Locale.IN, index=True)
    curriculum_board = Column(Enum(CurriculumBoard), nullable=False, default=CurriculumBoard.CBSE, index=True)
    grade_level = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('ix_bundles_locale_curriculum', 'locale', 'curriculum_board'),
        Index('ix_bundles_grade_level', 'grade_level'),
    )