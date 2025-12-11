from pydantic import BaseModel
from datetime import datetime

class GenerationJobBase(BaseModel):
    standard_id: int
    job_type: str
    status: str | None = None

class GenerationJobCreate(GenerationJobBase):
    pass

class GenerationJobRead(GenerationJobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True