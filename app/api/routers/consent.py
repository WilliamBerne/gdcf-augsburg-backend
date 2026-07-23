# app/api/routers/consent.py

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.consent import Consent
from app.models.document import Document
from app.models.member import Member
from app.schemas.consent import ConsentCreate, ConsentRead, ConsentUpdate

router = APIRouter(prefix="/consents", tags=["consents"])

_WITHDRAWAL_FIELDS = {
    "data_protection_consent": "data_protection_withdrawn_at",
    "newsletter_opt_in": "newsletter_withdrawn_at",
    "photo_video_consent": "photo_video_withdrawn_at",
}
_REVIEW_FIELDS = {
    "data_protection_signature_status": ("data_protection_reviewed_by", "data_protection_reviewed_at"),
    "photo_video_signature_status": ("photo_video_reviewed_by", "photo_video_reviewed_at"),
}


def _validate_signed_document(db: Session, member_id: int, document_id: int | None) -> None:
    if document_id is None:
        return
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Signed document not found")
    if document.member_id != member_id:
        raise HTTPException(status_code=400, detail="Signed document belongs to a different member")


def _set_initial_review_timestamps(consent: Consent) -> None:
    now = datetime.now(timezone.utc)
    for status_field, (_reviewer_field, reviewed_at_field) in _REVIEW_FIELDS.items():
        if getattr(consent, status_field) != "pending_review":
            setattr(consent, reviewed_at_field, now)


@router.post("/", response_model=ConsentRead, status_code=201)
def create_consent(payload: ConsentCreate, db: Session = Depends(get_db)):
    member = db.get(Member, payload.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    existing = db.query(Consent).filter(Consent.member_id == payload.member_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Consent record already exists for this member")

    _validate_signed_document(db, payload.member_id, payload.signed_document_id)
    consent = Consent(**payload.model_dump())
    _set_initial_review_timestamps(consent)
    db.add(consent)
    db.commit()
    db.refresh(consent)
    return consent


@router.get("/{consent_id}", response_model=ConsentRead)
def get_consent(consent_id: int, db: Session = Depends(get_db)):
    consent = db.get(Consent, consent_id)
    if not consent:
        raise HTTPException(status_code=404, detail="Consent record not found")
    return consent


@router.patch("/{consent_id}", response_model=ConsentRead)
def update_consent(consent_id: int, payload: ConsentUpdate, db: Session = Depends(get_db)):
    consent = db.get(Consent, consent_id)
    if not consent:
        raise HTTPException(status_code=404, detail="Consent record not found")

    changes = payload.model_dump(exclude_unset=True)
    if "signed_document_id" in changes:
        _validate_signed_document(db, consent.member_id, changes["signed_document_id"])

    now = datetime.now(timezone.utc)
    for field, value in changes.items():
        previous_value = getattr(consent, field)
        setattr(consent, field, value)

        withdrawal_field = _WITHDRAWAL_FIELDS.get(field)
        if withdrawal_field:
            if previous_value and not value:
                setattr(consent, withdrawal_field, now)
            elif value:
                setattr(consent, withdrawal_field, None)

        review_fields = _REVIEW_FIELDS.get(field)
        if review_fields:
            reviewer_field, reviewed_at_field = review_fields
            if value == "pending_review":
                setattr(consent, reviewer_field, None)
                setattr(consent, reviewed_at_field, None)
            else:
                setattr(consent, reviewed_at_field, now)

    db.commit()
    db.refresh(consent)
    return consent
