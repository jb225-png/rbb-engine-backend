from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from app.core.enums import Locale, CurriculumBoard, ProductType, ProductStatus

class ProductBase(BaseModel):
    standard_id: int
    generation_job_id: Optional[int] = None
    product_type: ProductType
    status: ProductStatus = ProductStatus.DRAFT
    locale: Locale = Locale.IN
    curriculum_board: CurriculumBoard = CurriculumBoard.CBSE
    grade_level: int

class ProductCreate(ProductBase):
    @field_validator('curriculum_board')
    @classmethod
    def validate_curriculum_board(cls, v, info):
        locale = info.data.get('locale', Locale.IN)
        if locale == Locale.IN and v != CurriculumBoard.CBSE:
            raise ValueError("India locale must use CBSE curriculum")
        if locale == Locale.US and v != CurriculumBoard.COMMON_CORE:
            raise ValueError("US locale must use Common Core curriculum")
        return v

    @field_validator('grade_level')
    @classmethod
    def validate_grade_level(cls, v):
        if not 1 <= v <= 12:
            raise ValueError("Grade level must be between 1 and 12")
        return v

class ProductRead(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
