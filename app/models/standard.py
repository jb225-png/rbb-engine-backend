from sqlalchemy import Column, Integer, String, DateTime, Index, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.enums import Locale, CurriculumBoard

class Standard(Base):
    """Educational standards that define content generation requirements"""
    __tablename__ = "standards"

    id = Column(Integer, primary_key=True, index=True)
    locale = Column(Enum(Locale), nullable=False, default=Locale.IN, index=True)
    curriculum_board = Column(Enum(CurriculumBoard), nullable=False, default=CurriculumBoard.CBSE, index=True)
    grade_level = Column(Integer, nullable=False, index=True)  # 1-12
    grade_range = Column(String, nullable=True)  # e.g., "6-8" for multi-grade standards
    code = Column(String, nullable=False, index=True)  # e.g., "CBSE.MATH.6.1" or "CCSS.MATH.1.OA.1"
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('ix_standards_locale_curriculum', 'locale', 'curriculum_board'),
        Index('ix_standards_grade_level', 'grade_level'),
        Index('ix_standards_code_unique', 'locale', 'curriculum_board', 'code', unique=True),
    )