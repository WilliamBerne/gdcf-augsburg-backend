# app/models/consent.py

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Consent(Base):
    """Data-protection, newsletter, and photo/video consents, one per member."""
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, unique=True)

    # Datenschutz
    data_protection_consent = Column(Boolean, nullable=False, default=False)
    data_protection_signed_name = Column(String(200), nullable=True)
    data_protection_signed_place = Column(String(100), nullable=True)
    data_protection_signed_date = Column(Date, nullable=True)

    newsletter_opt_in = Column(Boolean, nullable=False, default=False)

    # Foto/Video-Einwilligung
    photo_video_consent = Column(Boolean, nullable=False, default=False)
    photo_video_signed_name = Column(String(200), nullable=True)
    photo_video_signed_place = Column(String(100), nullable=True)
    photo_video_signed_date = Column(Date, nullable=True)

    # For minors: guardian must co-sign (and, from 14+, the minor signs too)
    guardian_signed_name = Column(String(200), nullable=True)
    minor_signed_name = Column(String(200), nullable=True)  # only used if member is 14–17

    member = relationship("Member", back_populates="consent")