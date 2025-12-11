from pydantic import BaseModel
from datetime import datetime

class StandardBase(BaseModel):
    code: str
    description: str | None = None

class StandardCreate(StandardBase):
    pass

class StandardRead(StandardBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True