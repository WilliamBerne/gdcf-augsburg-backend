# app/schemas/document.py

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    document_type: str
    file_path: str


class DocumentCreate(DocumentBase):
    member_id: int


class DocumentRead(DocumentBase):
    id: int
    member_id: int
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)