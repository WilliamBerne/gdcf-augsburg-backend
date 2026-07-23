# app/models/consent.py

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class Consent(Base):
    """Consent decisions plus human verification of the signed source form."""
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, unique=True)
    form_version = Column(String(100), nullable=False, default="gdcf-consent-de-zh-v1")
    signed_document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)


    # Datenschutz
    data_protection_consent = Column(Boolean, nullable=False, default=False)
    data_protection_signed_name = Column(String(200), nullable=True)
    data_protection_signed_place = Column(String(100), nullable=True)
    data_protection_signed_date = Column(Date, nullable=True)
    data_protection_signer_role = Column(String(20), nullable=True)
    data_protection_signature_status = Column(String(20), nullable=False, default="pending_review")
    data_protection_reviewed_by = Column(String(200), nullable=True)
    data_protection_reviewed_at = Column(DateTime(timezone=True), nullable=True)
    data_protection_withdrawn_at = Column(DateTime(timezone=True), nullable=True)


    newsletter_opt_in = Column(Boolean, nullable=False, default=False)
    newsletter_withdrawn_at = Column(DateTime(timezone=True), nullable=True)

    # Foto/Video-Einwilligung
    photo_video_consent = Column(Boolean, nullable=False, default=False)
    photo_video_signed_name = Column(String(200), nullable=True)
    photo_video_signed_place = Column(String(100), nullable=True)
    photo_video_signed_date = Column(Date, nullable=True)
    photo_video_signer_role = Column(String(20), nullable=True)
    photo_video_signature_status = Column(String(20), nullable=False, default="pending_review")
    photo_video_reviewed_by = Column(String(200), nullable=True)
    photo_video_reviewed_at = Column(DateTime(timezone=True), nullable=True)
    photo_video_withdrawn_at = Column(DateTime(timezone=True), nullable=True)


    photo_video_minor_co_signed = Column(Boolean, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    member = relationship("Member", back_populates="consent")
    signed_document = relationship("Document", foreign_keys=[signed_document_id])
