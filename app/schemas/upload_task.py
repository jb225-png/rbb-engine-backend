from pydantic import BaseModel
from datetime import datetime

class UploadTaskBase(BaseModel):
    product_id: int
    status: str | None = None

class UploadTaskCreate(UploadTaskBase):
    pass

class UploadTaskRead(UploadTaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UploadTaskUpdate(BaseModel):
    status: str