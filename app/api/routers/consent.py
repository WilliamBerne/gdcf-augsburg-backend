# app/api/routers/consent.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.member import Member
from app.models.consent import Consent
from app.schemas.consent import ConsentCreate, ConsentUpdate, ConsentRead

router = APIRouter(prefix="/consents", tags=["consents"])


@router.post("/", response_model=ConsentRead, status_code=201)
def create_consent(payload: ConsentCreate, db: Session = Depends(get_db)):
    member = db.get(Member, payload.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    existing = db.query(Consent).filter(Consent.member_id == payload.member_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Consent record already exists for this member")

    consent = Consent(**payload.model_dump())
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

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(consent, field, value)

    db.commit()
    db.refresh(consent)
    return consent