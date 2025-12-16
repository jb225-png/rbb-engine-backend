from pydantic import BaseModel
from typing import Literal

class GenerationRequestPayload(BaseModel):
    standard_code: str
    curriculum_board: str
    grade_level: str
    products: list[str]
    source: Literal["n8n"]