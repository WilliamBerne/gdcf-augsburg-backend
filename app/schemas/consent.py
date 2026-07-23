# app/schemas/consent.py

from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, model_validator


SignatureStatus = Literal["pending_review", "verified", "missing", "unclear"]
SignerRole = Literal["member", "guardian"]


class ConsentBase(BaseModel):
    form_version: str = "gdcf-consent-de-zh-v1"
    signed_document_id: Optional[int] = None

    data_protection_consent: bool = False
    data_protection_signed_name: Optional[str] = None
    data_protection_signed_place: Optional[str] = None
    data_protection_signed_date: Optional[date] = None
    data_protection_signer_role: Optional[SignerRole] = None
    data_protection_signature_status: SignatureStatus = "pending_review"
    data_protection_reviewed_by: Optional[str] = None

    newsletter_opt_in: bool = False

    photo_video_consent: bool = False
    photo_video_signed_name: Optional[str] = None
    photo_video_signed_place: Optional[str] = None
    photo_video_signed_date: Optional[date] = None
    photo_video_signer_role: Optional[SignerRole] = None
    photo_video_signature_status: SignatureStatus = "pending_review"
    photo_video_reviewed_by: Optional[str] = None

    photo_video_minor_co_signed: Optional[bool] = None

    @model_validator(mode="after")
    def require_reviewer_for_completed_review(self):
        pairs = (
            (self.data_protection_signature_status, self.data_protection_reviewed_by, "data_protection_reviewed_by"),
            (self.photo_video_signature_status, self.photo_video_reviewed_by, "photo_video_reviewed_by"),
        )
        missing = [name for status, reviewer, name in pairs if status != "pending_review" and not reviewer]
        if missing:
            raise ValueError(f"Reviewer is required for completed review: {', '.join(missing)}")
        return self


class ConsentCreate(ConsentBase):
    member_id: int


class ConsentUpdate(BaseModel):
    form_version: Optional[str] = None
    signed_document_id: Optional[int] = None
    data_protection_consent: Optional[bool] = None
    data_protection_signed_name: Optional[str] = None
    data_protection_signed_place: Optional[str] = None
    data_protection_signed_date: Optional[date] = None
    data_protection_signer_role: Optional[SignerRole] = None
    data_protection_signature_status: Optional[SignatureStatus] = None
    data_protection_reviewed_by: Optional[str] = None
    newsletter_opt_in: Optional[bool] = None
    photo_video_consent: Optional[bool] = None
    photo_video_signed_name: Optional[str] = None
    photo_video_signed_place: Optional[str] = None
    photo_video_signed_date: Optional[date] = None
    photo_video_signer_role: Optional[SignerRole] = None
    photo_video_signature_status: Optional[SignatureStatus] = None
    photo_video_reviewed_by: Optional[str] = None
    photo_video_minor_co_signed: Optional[bool] = None

    @model_validator(mode="after")
    def validate_update(self):
        non_nullable = {
            "form_version", "data_protection_consent", "data_protection_signature_status",
            "newsletter_opt_in", "photo_video_consent", "photo_video_signature_status",
        }
        null_fields = sorted(
            field for field in non_nullable & self.model_fields_set
            if getattr(self, field) is None
        )
        if null_fields:
            raise ValueError(f"Fields cannot be null: {', '.join(null_fields)}")

        pairs = (
            ("data_protection_signature_status", "data_protection_reviewed_by"),
            ("photo_video_signature_status", "photo_video_reviewed_by"),
        )
        missing = [
            reviewer for status, reviewer in pairs
            if status in self.model_fields_set
            and getattr(self, status) != "pending_review"
            and not getattr(self, reviewer)
        ]
        if missing:
            raise ValueError(f"Reviewer is required for completed review: {', '.join(missing)}")
        return self


class ConsentRead(ConsentBase):
    id: int
    member_id: int
    data_protection_reviewed_at: Optional[datetime] = None
    data_protection_withdrawn_at: Optional[datetime] = None
    newsletter_withdrawn_at: Optional[datetime] = None
    photo_video_reviewed_at: Optional[datetime] = None
    photo_video_withdrawn_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
