from pydantic import BaseModel
from app.core.enums import ProductType, Locale, CurriculumBoard

class GenerateProductRequest(BaseModel):
    standard_id: int
    product_type: ProductType
    locale: Locale = Locale.IN
    curriculum_board: CurriculumBoard = CurriculumBoard.CBSE
    grade_level: int

class GenerateProductResponse(BaseModel):
    job_id: int
    product_ids: list[int]
    message: str