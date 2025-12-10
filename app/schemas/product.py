from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    title: str
    status: str | None = None

class ProductRead(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
