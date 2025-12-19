from pydantic import BaseModel
from datetime import datetime
from app.core.enums import UploadTaskStatus

class UploadTaskBase(BaseModel):
    product_id: int
    status: UploadTaskStatus | None = None
    assigned_to: str | None = None

class UploadTaskCreate(UploadTaskBase):
    pass

class UploadTaskRead(UploadTaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UploadTaskUpdate(BaseModel):
    status: UploadTaskStatus | None = None
    assigned_to: str | None = None