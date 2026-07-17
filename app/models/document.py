# app/models/document.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Document(Base):
    """Uploaded scans of signed forms (application, SEPA mandate, consent, etc.)."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)

    document_type = Column(String(100), nullable=False)   # e.g. "application", "sepa_mandate", "consent"
    file_path = Column(String(500), nullable=False)        # or storage key/URL
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    member = relationship("Member", back_populates="documents")